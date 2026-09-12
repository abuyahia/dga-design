#!/usr/bin/env python3
"""Dependency-free repository audit. Never evaluates authored JS/check expressions."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def strip_comments(css):
    return re.sub(r'/\*.*?\*/', lambda m: '\n' * m[0].count('\n'), css, flags=re.S)


def schema_errors(value, schema, at='$'):
    """Validate exactly the keyword subset used by our checked-in schemas.

    Not a general JSON Schema implementation. Unknown validation keywords fail closed.
    """
    supported = {'$schema', 'title', 'description', 'type', 'required', 'properties',
                 'additionalProperties', 'items', 'uniqueItems', 'minItems', 'minLength', 'enum', 'const'}
    errors = [f'{at}: unsupported schema keyword {key}' for key in schema if key not in supported]
    types = {'object': dict, 'array': list, 'string': str}
    typ = schema.get('type')
    if typ and (typ not in types or not isinstance(value, types[typ])):
        return errors + [f'{at}: expected {typ}']
    if 'const' in schema and value != schema['const']:
        errors.append(f'{at}: expected {schema["const"]!r}')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{at}: value outside enum')
    if isinstance(value, str) and len(value) < schema.get('minLength', 0):
        errors.append(f'{at}: string too short')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                errors.append(f'{at}: missing {key}')
        props = schema.get('properties', {})
        for key, child in value.items():
            if key in props:
                errors.extend(schema_errors(child, props[key], f'{at}.{key}'))
            elif isinstance(schema.get('additionalProperties'), dict):
                errors.extend(schema_errors(child, schema['additionalProperties'], f'{at}.{key}'))
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(f'{at}: array too short')
        if schema.get('uniqueItems') and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            errors.append(f'{at}: duplicate items')
        for i, item in enumerate(value):
            errors.extend(schema_errors(item, schema.get('items', {}), f'{at}[{i}]'))
    return errors


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and 'stylesheet' in attrs.get('rel', '').split():
            self.assets.append((attrs.get('href', ''), self.getpos()[0]))
        if tag == 'script' and attrs.get('src'):
            self.assets.append((attrs['src'], self.getpos()[0]))


def read_json(path):
    def no_duplicates(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=no_duplicates)


def audit(root):
    issues = []
    documents = {}
    def issue(level, code, path, detail, line=None):
        item = {'severity': level, 'code': code, 'path': str(path.relative_to(root)), 'detail': detail}
        if line is not None:
            item['line'] = line
        issues.append(item)

    # Only source directories: no .git, user settings, generated reports or dependencies.
    for folder in ['components', 'standards', 'docs']:
        for path in sorted((root / folder).rglob('*.json')):
            if 'reports' in path.relative_to(root).parts:
                continue
            try:
                documents[path] = read_json(path)
            except (ValueError, OSError) as exc:
                issue('error', 'json_invalid', path, str(exc))

    ref_schema = documents.get(root / 'standards/schemas/component-reference.schema.json')
    audit_schema = documents.get(root / 'standards/schemas/component-audit.schema.json')
    registry = documents.get(root / 'standards/audit-rule-types.json', {})
    known_types = {r['type'] for r in registry.get('rule_types', [])}
    deferred = []
    for pattern, schema in [('*/reference.json', ref_schema), ('*/audit-rules.json', audit_schema)]:
        if schema is None:
            issue('error', 'schema_missing', root / 'standards/schemas', pattern)
            continue
        for path in sorted((root / 'components').glob(pattern)):
            data = documents.get(path)
            if data is None:
                continue
            errors = schema_errors(data, schema)
            for error in errors:
                issue('error', 'schema_invalid', path, error)
            if errors:
                continue
            schema_path = data.get('$schema')
            if not schema_path or not (path.parent / schema_path).is_file():
                issue('error', 'schema_link_invalid', path, str(schema_path))
            if path.name == 'reference.json':
                if data['component']['name'] != path.parent.name:
                    issue('error', 'component_name_mismatch', path, data['component']['name'])
                if set(data['axes']) != set(data['axis_values']):
                    issue('error', 'axis_values_mismatch', path, 'axes and axis_values keys differ')
                ids = [v['id'] for v in data['variants']]
                if len(ids) != len(set(ids)):
                    issue('error', 'duplicate_variant_id', path, 'Variant IDs must be unique within the package')
                for v in data['variants']:
                    for axis, value in v.get('axes', {}).items():
                        if axis not in data['axis_values'] or value not in data['axis_values'][axis]:
                            issue('error', 'variant_axis_invalid', path, f'{v["id"]}: {axis}={value!r}')
                    for key, value in v.get('files', {}).items():
                        if isinstance(value, str) and not (path.parent / value).exists():
                            issue('warning', 'source_file_missing', path, f'{v["id"]}.{key}: {value}')
            else:
                if data['component_id'] != path.parent.name:
                    issue('error', 'component_name_mismatch', path, data['component_id'])
                if (path.parent / data['rule_types_registry']).resolve() != (root / 'standards/audit-rule-types.json').resolve():
                    issue('error', 'registry_link_invalid', path, data['rule_types_registry'])
                ids = [r['id'] for r in data['rules']]
                if len(ids) != len(set(ids)):
                    issue('error', 'duplicate_rule_id', path, 'Rule IDs must be unique within the package')
                for rule in data['rules']:
                    if rule['rule_type'] not in known_types:
                        issue('error', 'rule_type_unknown', path, rule['rule_type'])
                    deferred.append({'component': path.parent.name, 'id': rule['id'],
                        'rule_type': rule['rule_type'], 'status': 'not_run',
                        'reason': 'Authored component rule requires a dedicated interpreter or browser/manual review.'})

    inventory = documents.get(root / 'docs/inventory.json', {})
    inventory_schema = documents.get(root / 'standards/schemas/inventory.schema.json')
    inventory_errors = schema_errors(inventory, inventory_schema) if inventory_schema else ['Inventory schema missing']
    for error in inventory_errors:
        issue('error', 'inventory_schema_invalid', root / 'docs/inventory.json', error)
    entries = inventory.get('items', []) if not inventory_errors else []
    index = {e['id']: e for e in entries}
    inv_path = root / 'docs/inventory.json'
    if not entries or len(index) != len(entries):
        issue('error', 'inventory_invalid', inv_path, 'Missing inventory or duplicate IDs')
    for entry in entries:
        if entry['status'] == 'planned' and (entry['path'] or entry['files'] or entry['production_ready']):
            issue('error', 'planned_claim_invalid', inv_path, entry['id'])
        if entry['path'] and not (root / entry['path']).is_dir():
            issue('error', 'inventory_path_missing', inv_path, entry['path'])
        if entry.get('replacement') and entry['replacement'] not in index:
            issue('error', 'replacement_missing', inv_path, entry['id'])
        for dep in entry['dependencies']:
            if dep not in index:
                issue('error', 'dependency_missing', inv_path, f'{entry["id"]} -> {dep}')
        for name, value in entry.get('files', {}).items():
            if value and not (root / value).is_file():
                issue('error', 'inventory_file_missing', inv_path, f'{entry["id"]}.{name}: {value}')
    selected = Counter(e['semantic_id'] for e in entries if e['selection'] == 'canonical')
    for semantic_id, count in selected.items():
        if count > 1:
            issue('error', 'duplicate_canonical', inv_path, semantic_id)
    visiting, visited = set(), set()
    def visit(key):
        if key in visiting:
            issue('error', 'dependency_cycle', inv_path, key)
            return
        if key in visited or key not in index:
            return
        visiting.add(key)
        for dep in index[key]['dependencies']:
            visit(dep)
        visiting.remove(key)
        visited.add(key)
    for key in index:
        visit(key)
    actual = {str(p.relative_to(root)) for p in (root / 'components').iterdir() if p.is_dir() and p.name != '_showcase'}
    recorded = {e['path'] for e in entries if e.get('path', '').startswith('components/')}
    for missing in actual - recorded:
        issue('error', 'inventory_package_missing', inv_path, missing)

    token_path = root / 'token.css'
    token_css = strip_comments(token_path.read_text())
    definitions = set(re.findall(r'(--[\w-]+)\s*:', token_css))
    for name in sorted(set(re.findall(r'var\(\s*(--[\w-]+)', token_css)) - definitions):
        issue('error', 'token_alias_missing', token_path, name)
    policy = documents.get(root / 'standards/foundation-policy.json', {})
    local_properties = {(e['path'], e['name']): e for e in policy.get('local_custom_properties', [])}
    exceptions = policy.get('css_exceptions', [])
    for entry in [*local_properties.values(), *exceptions]:
        if not entry.get('reason') or not (root / entry['path']).is_file():
            issue('error', 'foundation_policy_invalid', root / 'standards/foundation-policy.json', str(entry))
    for entry in exceptions:
        path = root / entry['path']
        if path.is_file() and 'occurrences' in entry:
            pattern = r'\s*' + re.escape(entry['property']) + r'\s*:\s*' + re.escape(entry['value']) + r'\s*;\s*'
            count = sum(bool(re.fullmatch(pattern, line)) for line in strip_comments(path.read_text()).splitlines())
            if count != entry['occurrences']:
                issue('error', 'exception_scope_changed', path, f'{entry["property"]}: {entry["value"]} occurred {count} times')
    def exempt(path, line):
        for e in exceptions:
            if str(path.relative_to(root)) == e['path'] and re.fullmatch(r'\s*' + re.escape(e['property']) + r'\s*:\s*' + re.escape(e['value']) + r'\s*;\s*', line):
                return True
        return False
    # Verify central aliases transitively; a cycle is invalid even if every name exists.
    token_values = dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', token_css))
    complete = set()
    def resolve_token(name, active=()):
        if name in active:
            issue('error', 'token_cycle', token_path, ' -> '.join((*active, name)))
            return
        if name in complete:
            return
        for dep in re.findall(r'var\(\s*(--[\w-]+)', token_values.get(name, '')):
            resolve_token(dep, (*active, name))
        complete.add(name)
    for name in token_values:
        resolve_token(name)
    for bp in policy.get('breakpoint_rules', []):
        path = root / bp['path']
        condition = bp['condition']
        value = token_values.get(bp['token'], '').strip()
        if bp.get('adjustment_px') and re.fullmatch(r'\d+px', value):
            value = f"{int(value[:-2]) + bp['adjustment_px']}px"
        comparison = bp.get('comparison', 'min-width')
        if not path.is_file() or condition not in path.read_text() or condition != f'({comparison}: {value})':
            issue('error', 'breakpoint_mismatch', path, f'{condition} must match {bp["token"]}')
    for path in sorted([*(root / 'components').glob('*/*.css'), *(root / 'styles/base').glob('*.css')]):
        if path.parent.name == '_showcase':
            continue
        css = strip_comments(path.read_text())
        if 'components' in path.relative_to(root).parts:
            for name in set(re.findall(r'(?<![\w.-])(--[\w-]+)\s*:', css)):
                if (str(path.relative_to(root)), name) not in local_properties:
                    issue('warning', 'unregistered_local_definition', path, name)
        for name in sorted(set(re.findall(r'var\(\s*(--[\w-]+)', css)) - definitions):
            entry = local_properties.get((str(path.relative_to(root)), name))
            if entry and entry['kind'] == 'variant_binding' and not re.search(re.escape(name) + r'\s*:', css):
                issue('error', 'local_binding_missing', path, name)
            elif not entry:
                issue('warning', 'token_not_central', path, name)
        # A source heuristic: comments excluded; literals include fallback values.
        # Zero/unitless structural values and SVG path data are not token candidates.
        for line_no, line in enumerate(css.splitlines(), 1):
            if (re.search(r'(?<![\w-])(?:left|right|margin-left|margin-right|padding-left|padding-right|border-left|border-right)\s*:', line) or re.search(r'(?:text-align|transform-origin)\s*:\s*(?:left|right)\b', line)) and not exempt(path, line):
                issue('warning', 'physical_css_review', path, line.strip(), line_no)
            if ':' in line and not line.lstrip().startswith('@') and re.search(r'#[\da-fA-F]{3,8}\b|\b(?:rgb|hsl)a?\(|(?<![\w-])\d*\.?\d+(?:px|rem|ms|s)\b|font-weight\s*:\s*[1-9]\d*', line) and not exempt(path, line):
                issue('warning', 'visual_literal_review', path, line.strip(), line_no)

    for path in sorted([*(root / 'components').rglob('*.html'), *(root / 'tests/fixtures').rglob('*.html')]):
        parser = Assets()
        parser.feed(path.read_text())
        for url, line in parser.assets:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path or '{{' in url:
                continue
            target = root / unquote(parsed.path.lstrip('/')) if parsed.path.startswith('/') else path.parent / unquote(parsed.path)
            if not target.is_file():
                issue('error', 'asset_missing', path, url, line)

    return {'audit_version': '1.0.0', 'scope': 'repository_static',
        'production_ready': False, 'summary': dict(Counter(i['severity'] for i in issues)),
        'checks': ['json_parse', 'reference_schema', 'audit_schema', 'rule_registry', 'inventory_dependencies', 'token_references', 'css_source_review', 'html_css_js_assets'],
        'limitations': ['Not a CSS parser or computed-style test.', 'Does not execute component audit rules.',
                        'Does not verify keyboard, contrast, responsive layout, ARIA behavior or official compliance.',
                        'Source paths in prose/Figma payloads are not treated as executable asset links.'],
        'issues': issues, 'component_rules': deferred}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, help='Write JSON report; does not change compliance files')
    parser.add_argument('--strict', action='store_true', help='Also fail on warnings; use for later Foundation readiness')
    args = parser.parse_args()
    report = audit(args.root.resolve())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    counts = report['summary']
    print(f"Repository audit: {counts.get('error', 0)} errors, {counts.get('warning', 0)} warnings; {len(report['component_rules'])} component rules NOT RUN.")
    for item in report['issues']:
        if item['severity'] == 'error':
            print(f"ERROR {item['code']} {item['path']}: {item['detail']}")
    return 1 if counts.get('error') or (args.strict and counts.get('warning')) else 0


if __name__ == '__main__':
    sys.exit(main())
