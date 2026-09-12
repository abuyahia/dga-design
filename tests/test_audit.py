"""Regression checks for the audit tool, not visual/component certification."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit', ROOT / 'scripts/audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'standards', self.root / 'standards')
        (self.root / 'standards/foundation-policy.json').write_text('{}')
        (self.root / 'components/example').mkdir(parents=True)
        (self.root / 'docs').mkdir()
        (self.root / 'token.css').write_text(':root { --color: black; }')
        (self.root / 'components/example/example.css').write_text('.example { color: var(--color); }')
        self.write('docs/inventory.json', {'schema_version': '1.0.0', 'items': [{
            'id': 'example', 'semantic_id': 'example', 'layer': 'core',
            'path': 'components/example', 'status': 'needs_improvement', 'selection': 'canonical',
            'production_ready': False, 'dependencies': [], 'files': {'css': 'components/example/example.css'}
        }]})
        self.write('components/example/reference.json', {
            '$schema': '../../standards/schemas/component-reference.schema.json',
            'schema_version': '2.1.0', 'component': {'name': 'example'},
            'axes': ['size'], 'axis_values': {'size': ['small']},
            'variants': [{'id': 'small', 'axes': {'size': 'small'}}], 'variant_coverage': 'documented_subset'
        })

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value))

    def codes(self):
        return {i['code'] for i in audit.audit(self.root)['issues']}

    def test_clean_repository_has_no_issues(self):
        self.assertEqual(audit.audit(self.root)['issues'], [])

    def test_invalid_json_is_reported(self):
        (self.root / 'components/example/reference.json').write_text('{')
        self.assertIn('json_invalid', self.codes())

    def test_duplicate_json_keys_are_rejected(self):
        (self.root / 'components/example/reference.json').write_text('{"a":1,"a":2}')
        self.assertIn('json_invalid', self.codes())

    def test_schema_and_axis_values_are_enforced(self):
        p = self.root / 'components/example/reference.json'
        d = json.loads(p.read_text())
        d['variants'][0]['axes']['size'] = 'large'
        p.write_text(json.dumps(d))
        self.assertIn('variant_axis_invalid', self.codes())
        d['axes'] = {'size': []}
        p.write_text(json.dumps(d))
        self.assertIn('schema_invalid', self.codes())

    def test_unknown_rule_and_unexecuted_rule_are_not_passes(self):
        self.write('components/example/audit-rules.json', {
            '$schema': '../../standards/schemas/component-audit.schema.json',
            'schema_version': '1.1.0', 'component_id': 'example',
            'rule_types_registry': '../../standards/audit-rule-types.json',
            'rules': [{'id': 'EX-1', 'rule_type': 'invented', 'severity': 'error', 'validation_status': 'not_run'}]
        })
        result = audit.audit(self.root)
        self.assertIn('rule_type_unknown', {i['code'] for i in result['issues']})
        self.assertEqual(result['component_rules'][0]['status'], 'not_run')

    def test_css_comments_do_not_define_tokens_or_trigger_findings(self):
        (self.root / 'components/example/example.css').write_text(
            '/* --missing: red; left: 12px; var(--comment-only) */\n.example {color:var(--missing, #fff);}')
        result = audit.audit(self.root)
        missing = [i['detail'] for i in result['issues'] if i['code'] == 'token_not_central']
        self.assertEqual(missing, ['--missing'])
        self.assertNotIn('physical_css_review', self.codes())

    def test_missing_local_asset_and_remote_exclusion(self):
        (self.root / 'components/example/template.html').write_text(
            '<link rel="stylesheet" href="missing.css"><script src="https://example.com/a.js"></script>')
        issues = [i for i in audit.audit(self.root)['issues'] if i['code'] == 'asset_missing']
        self.assertEqual(len(issues), 1)

    def test_dependencies_missing_and_cyclic(self):
        p = self.root / 'docs/inventory.json'
        d = json.loads(p.read_text())
        d['items'][0]['dependencies'] = ['example', 'missing']
        p.write_text(json.dumps(d))
        self.assertTrue({'dependency_cycle', 'dependency_missing'} <= self.codes())

    def test_malformed_inventory_reports_error_without_crash(self):
        self.write('docs/inventory.json', {'items': [{}]})
        self.assertIn('inventory_schema_invalid', self.codes())

    def test_cli_warning_policy_and_strict_failure(self):
        (self.root / 'components/example/example.css').write_text('.example {color:var(--missing);}')
        args = [sys.executable, str(ROOT / 'scripts/audit.py'), '--root', str(self.root)]
        self.assertEqual(subprocess.run(args, capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(args + ['--strict'], capture_output=True).returncode, 1)
        (self.root / 'components/example/reference.json').write_text('{')
        self.assertEqual(subprocess.run(args, capture_output=True).returncode, 1)

    def test_token_cycles_are_errors(self):
        (self.root / 'token.css').write_text(':root {--color: var(--other); --other: var(--color);}')
        self.assertIn('token_cycle', self.codes())

    def test_bem_pseudo_selector_is_not_a_custom_property(self):
        (self.root / 'components/example/example.css').write_text('.example--primary:focus { color: var(--color); }')
        self.assertNotIn('unregistered_local_definition', self.codes())

    def test_local_binding_requires_definition_and_exact_registration(self):
        self.write('standards/foundation-policy.json', {'local_custom_properties': [{
            'path': 'components/example/example.css', 'name': '--slot', 'kind': 'variant_binding', 'reason': 'Variant selection.'
        }]})
        p = self.root / 'components/example/example.css'
        p.write_text('.example { color: var(--slot); }')
        self.assertIn('local_binding_missing', self.codes())
        p.write_text('.example { --slot: var(--color); color: var(--slot); }')
        self.assertNotIn('token_not_central', self.codes())
        p.write_text('.example { --slot: var(--color); --new: red; color: var(--new); }')
        self.assertIn('unregistered_local_definition', self.codes())
        self.assertIn('token_not_central', self.codes())

    def test_exception_does_not_suppress_changed_or_extra_declarations(self):
        self.write('standards/foundation-policy.json', {'css_exceptions': [{
            'path': 'components/example/example.css', 'property': 'left', 'value': '50%', 'reason': 'Physical centering.'
        }]})
        p = self.root / 'components/example/example.css'
        p.write_text('.example {\n left: 50%;\n}')
        self.assertNotIn('physical_css_review', self.codes())
        p.write_text('.example {\n left: 51%;\n}')
        self.assertIn('physical_css_review', self.codes())
        p.write_text('.example {\n left: 50%; width: 18px;\n}')
        self.assertIn('visual_literal_review', self.codes())

    def test_breakpoint_must_follow_token_value(self):
        self.write('standards/foundation-policy.json', {'breakpoint_rules': [{
            'path': 'components/example/example.css', 'condition': '(min-width: 768px)', 'token': '--bp-tablet'
        }]})
        (self.root / 'token.css').write_text(':root {--color: black; --bp-tablet: 768px;}')
        (self.root / 'components/example/example.css').write_text('@media (min-width: 768px) {}')
        self.assertNotIn('breakpoint_mismatch', self.codes())
        (self.root / 'token.css').write_text(':root {--color: black; --bp-tablet: 769px;}')
        self.assertIn('breakpoint_mismatch', self.codes())


if __name__ == '__main__':
    unittest.main()
