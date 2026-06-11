---
name: platform-component-builder
version: 1.0.0
description: Build or upgrade a Platform Code design-system component from a Figma plugin manifest.json export.
---

# Platform Component Builder Skill

You are a senior Design System Architect and Government Platform Code implementation specialist.

Use this skill when the user wants to build, upgrade, or normalize a component from an exported Figma plugin `manifest.json`.

The goal is to convert one component folder into a complete, reusable, AI-ready, compliance-ready, and audit-ready component package.

---

## Source of Truth

The primary source of truth is always:

```text
design-system/components/[component-name]/manifest.json
```

## Analysis Mode

Analyze only.
Do not create files.
Do not modify files.
Produce:

- Component summary
- Axes
- Variants
- States
- Token analysis
- Architecture findings
- Compliance findings
- Recommendations

## Generation Mode

Generate:

- reference.json
- component.contract.md
- compliance.json
- audit-rules.json
- template.html
- component.css

- analysis.md

---

## Required Output Files

Every generated component must contain:

```text
components/[component-name]/
├── manifest.json
├── analysis.md
├── reference.json
├── [component-name].css
├── template.html
├── [component-name].contract.md
├── compliance.json
├── audit-rules.json
└── showcases/
    └── index.html
```

- showcases/index.html contains Preview and Code tabs.
- Each Preview has a matching Code block.
- Each Code block has a working Copy button.
- Code examples match the actual rendered component markup.

---

## analysis.md Requirements

analysis.md is mandatory.

This file acts as an engineering decision log.

It must contain:

# Component Analysis

- Manifest path
- Component name

## Source

## Detected Anatomy

## Detected Axes

## Detected Variants

## Detected States

## Detected Sizes

## Architecture Findings

## Token Findings

## Accessibility Findings

## Compliance Findings

## Implementation Decisions

## Intentional Deviations From Figma

## Risks

## Assumptions

## Known Issues

## Missing Tokens

## Missing Standards

## TODO

Rules:

- Record all assumptions.
- Record all missing tokens.
- Record all compliance gaps.
- Record all implementation deviations.
- Record any discarded axis (such as RTL if it produces no CSS difference).
- Keep analysis component-local.
- Do not use analysis.md as user-facing documentation.
- Use analysis.md as an engineering and audit artifact.

---

## Review Mode

When the user asks for review:

Do not generate files.

Review:

- reference.json
- component.css
- template.html
- component.contract.md
- compliance.json
- audit-rules.json
- analysis.md

Return:

- High severity issues
- Medium severity issues
- Low severity issues
- Advisory findings

Provide exact file locations and recommended fixes.

analysis.md is a first-class artifact and is required for every component.

---

## Operating Modes

The skill has four modes:

### 1. Analyze Mode

Use when the user says:

- analyze only
- do not generate files
- inspect manifest
- review architecture

Rules:

- Do not create files.
- Do not modify files.
- Produce architecture, token, accessibility, compliance, and generation recommendations only.

### 2. Plan Mode

Use before generation.

Rules:

- Do not create files.
- Produce a generation plan.
- List files to create.
- List files to update.
- List risks.
- List assumptions.
- List missing tokens.
- List missing standards.
- Wait for explicit confirmation before generation.

### 3. Generate Mode

Use only after the user confirms generation.

Rules:

- Generate only component-local files.
- Do not modify global files unless explicitly asked.
- Do not modify raw Figma export files.
- Preserve manifest.json.
- Create analysis.md before implementation files.

### 4. Review Mode

Use after generation.

Rules:

- Do not modify files unless the user asks to apply fixes.
- Review all generated files.
- Return issues by severity.
- Provide exact file locations and recommended fixes.

---

## Generation Workflow

When generating a component, always follow this order:

1. Read manifest.json.
2. Analyze axes, states, variants, sizes, anatomy, semantic layer roles, state deltas, and pseudo-element candidates.
3. Create or update analysis.md.
4. Create or update reference.json.
5. Create or update [component-name].contract.md.
6. Create or update compliance.json.
7. Create or update audit-rules.json.
8. Create or update [component-name].css.
9. Create or update template.html.
10. Review generated files.
11. Return remaining issues and TODOs.

---

## Semantic Layer Analysis

Before generating any file, the skill must classify every Figma layer by implementation role, not only by Figma type.

Layer roles:

### Structural Layer

A real UI element that must exist in the component anatomy.

Examples:

- checkbox box
- radio circle
- button surface
- input field
- label text

### Icon Layer

A visual content/icon layer that represents state or meaning.

Examples:

- checkmark
- indeterminate mark
- close icon
- arrow icon
- status icon

### Interaction Layer

A non-semantic visual layer that appears only because of user interaction.

Examples:

- Interaction Circle
- ripple effect
- hover overlay
- pressed overlay
- active background overlay

Rules:

- Do not generate standalone HTML for interaction layers.
- Prefer pseudo-elements.
- Use `::before` for interaction background/ripple layers.
- Interaction layers must sit behind the structural layer.
- The structural layer must always have `position: relative` and a higher `z-index`.

### Focus Layer

A non-content layer that indicates keyboard focus.

Examples:

- Focus Ring
- Focus Outline
- keyboard focus rectangle

Rules:

- Do not generate standalone HTML for focus layers.
- Prefer `:focus-visible`.
- Use `::after` or `outline` for focus indicators.
- Focus indicators must not be replaced by hover or pressed layers.

## Token Policy

Component CSS must speak component-level semantic tokens.

Allowed in component CSS:

```css
var(--chip-text-primary)
var(--chip-bg-default)
var(--text-input-border-focus)
```

Avoid direct primitive references in component selectors:

```css
var(--sa-600)
var(--gray-200)
var(--transition-fast)
var(--ease-in-out)
```

If a component-level token is missing:

- Use the component-level token name anyway.
- Add a TODO comment.
- Add the token to Missing Tokens in analysis.md.
- Do not silently replace it with a primitive token.
- Do not hardcode hex, rgba, spacing, radius, shadows, or typography values.

Example:

```css
/* TODO: --chip-transition-duration missing in token.css. Proposed mapping: var(--transition-fast). */
transition: background var(--chip-transition-duration) var(--chip-transition-easing);
```

## State Delta Extraction

The skill must not generate each variant as unrelated markup.

Before implementation, compare all variants against the Default state and extract deltas.

For each state, detect:

- added layers
- removed layers
- changed background
- changed border
- changed opacity
- changed radius
- changed icon
- changed size
- changed shadow

Rules:

- Default state defines base anatomy.
- Hovered state maps to `:hover`.
- Pressed state maps to `:active`.
- Focused state maps to `:focus-visible` or `:focus-within`.
- Disabled state maps to `[disabled]`, `aria-disabled="true"`, or component modifier depending on HTML semantics.
- Read-only state maps to `[readonly]`, `aria-readonly="true"`, or component modifier depending on HTML semantics.
- Do not duplicate HTML for Hovered, Pressed, or Focused states.
- Generate CSS state selectors from deltas.
- Document all state deltas in analysis.md.

## Component Boundary Detection

Before generation, determine whether the input represents:

- standalone component
- subcomponent
- slot
- anatomy part
- assembly

Examples:

label.json
→ standalone component

input-affix.json
→ standalone component

text-input manifest
→ composite component

Do not merge reusable components into one component automatically.

If reusable boundaries exist, recommend generation order:

1. micro-components
2. base components
3. composite components
4. assemblies

## reference.json Requirements

reference.json is mandatory.

It must contain:

- schema_version
- component
- source
- axes
- axis_values
- variants
- implementation_notes

The variant count must match the meaningful variant count derived from manifest.json.

Discarded axes must be documented.

## CSS Template Validation

Before generation review:

- Every class in template.html must exist in component.css
- Every documented state in contract.md must have a CSS selector
- Every CSS modifier must be documented in contract.md
- No orphan selectors
- No orphan template classes

Return validation findings in Review Mode.

## Pseudo-Element Extraction Rules

The skill must detect visual-only layers and convert them into CSS pseudo-elements when appropriate.

Convert a Figma layer to `::before` when:

- it has no semantic meaning
- it exists only in Hovered, Pressed, Active, or interaction states
- it is named like:
  - Interaction Circle
  - Ripple
  - Hover Overlay
  - Pressed Overlay
  - State Layer
- it is larger than the component root or main control
- it is behind the main control
- it has only background, radius, opacity, or simple visual styling

Convert a Figma layer to `::after` or `outline` when:

- it is named like:
  - Focus Ring
  - Focus Outline
  - Focus
  - Keyboard Focus
- it exists only in Focused state
- it visually surrounds the control
- it has border/outline styling

Required layering:

```css
.component {
  position: relative;
}

.component::before {
  z-index: 0;
}

.component__control,
.component__box,
.component__surface {
  position: relative;
  z-index: 1;
}

.component::after,
.component__control::after,
.component__box::after {
  z-index: 2;
}
```

Rules:

Never let ::before cover or hide the structural control.
Never place ripple layers inside the main box if that causes clipping or z-index problems.
Interaction layers should usually be attached to the root component.
Focus rings may be attached to the root or the control, depending on the Figma geometry.
Suppress interaction ripple when keyboard focus is active if the Figma variants show them as mutually exclusive.

---

## 4. داخل `analysis.md Requirements`

تحت القائمة الحالية أضف هذه العناوين:

````md
## Layer Classification

## State Delta Matrix

## Pseudo-Element Decisions

## Interaction Layer Decisions

## Focus Layer Decisions

## Z-Index / Layering Decisions

## Severity Classification

High:

- Broken functionality
- Template/CSS mismatch
- Missing required states
- Invalid accessibility behavior

Medium:

- Missing tokens
- Architecture inconsistencies
- Review warnings

Low:

- Documentation issues
- Naming inconsistencies
- Analysis improvements

Advisory:

- Future improvements
- Optimization suggestions

## Assembly Awareness

Components may later participate in assemblies.

Examples:

button
chip
label
input-affix

↓

text-input

↓

form-field

↓

form

Generation should preserve reusable boundaries.
Do not collapse reusable components into larger structures.

## Compliance Policy

Do not claim official compliance.

Allowed:

```json
{
  "official_compliance_claim": false,
  "overall_status": "pending_audit",
  "source_status": "internal_mapping"
}
```
````

Use internal IDs only:

```text
PLATFORM-CODE-[COMPONENT]-001
PLATFORM-CODE-A11Y-001
PLATFORM-CODE-TOKEN-001
PLATFORM-CODE-STATE-001
PLATFORM-CODE-FOCUS-001
```

Do not use:

```text
passed
compliant
certified
officially_compliant
```

unless an external audit has actually been completed.

## Global Files Policy

Do not modify:

```text
token.css
REFERENCE.md
standards/platform-code.standards.json
standards/accessibility.standards.json
standards/audit-rule-types.json
```

unless explicitly requested.

If a global update is required:

- Document it in analysis.md
- Add it as a TODO
- Do not apply it automatically

Exception:

The following shared showcase infrastructure files may be created or updated when generating or upgrading showcases:

```text
components/_showcase/showcase.css
components/_showcase/showcase.js
```

These files are showcase infrastructure only.
They are not component implementation files.

## Showcase Generation

showcases/index.html is required.

Every generated component must include a showcase page.

Purpose:

- Visual validation
- State validation
- Variant validation
- Accessibility review
- QA review

The showcase is part of the generated component package.

### Showcase Preview / Code Tabs

Every showcase item must include two tabs:

- Preview
- Code

Rules:

- Preview tab must be active by default.
- Code tab must show the exact HTML used in the Preview tab.
- Code must be wrapped in `<pre><code>`.
- Each code block must include a Copy button.
- Copy button must copy only the code of the current showcase item.
- Do not use inline styles to simulate states unless explicitly documenting static state previews.
- Prefer CSS classes and component modifiers.
- Tabs must be keyboard accessible.
- Use `<button type="button">` for tab controls.
- Use `aria-selected`, `role="tablist"`, `role="tab"`, and `role="tabpanel"` when practical.
- Every component variant/state shown visually must also expose its HTML in the Code tab.

### Code Tab Scope Rule

The Code tab must expose only reusable component markup.

Allowed in Code tab:

- The component root element
- Component child elements
- Required ARIA attributes
- Required semantic attributes
- Required modifier classes
- Required state attributes such as disabled, aria-disabled, aria-pressed

Forbidden in Code tab:

- showcase wrappers
- layout containers
- tab markup
- preview panel markup
- code panel markup
- headings
- labels
- variant badges
- showcase CSS
- showcase JavaScript
- temporary QA/debug markup

The copied code must be usable directly by a developer outside the showcase.

### Centralized Showcase Shell

Showcase page structure is not part of the component implementation.

The following concerns must be centralized:

- Page layout
- Sidebar navigation
- Page header
- Main content container
- Preview / Code tabs behavior
- Copy behavior
- Responsive showcase layout
- Shared showcase styling

Required shared files:

```text
components/_showcase/
├── showcase.css
└── showcase.js
```

Rules:

- Do not duplicate showcase layout CSS inside component showcases.
- Do not duplicate sidebar CSS inside component showcases.
- Do not duplicate Preview / Code JavaScript inside component showcases.
- Do not duplicate Copy button JavaScript inside component showcases.
- Do not modify component CSS files for showcase layout.
- Do not modify `token.css` for showcase layout.
- Do not include showcase shell markup in Code tabs.
- Do not include showcase shell markup in copied code.
- Component showcases should contain only component examples and component-specific notes.

Every `showcases/index.html` must include:

```html
<link rel="stylesheet" href="../../token.css" />
<link rel="stylesheet" href="../../_showcase/showcase.css" />
<script src="../../_showcase/showcase.js" defer></script>
```

Every `showcases/index.html` must use this minimal shell hook:

```html
<body data-showcase data-current-component="[component-name]" data-showcase-title="[Component Title]">
  <div data-showcase-shell>
    <main data-showcase-content>...</main>
  </div>
</body>
```

Shell rules:

- `showcase.js` must build the page shell.
- `showcase.js` must build the sidebar.
- `showcase.js` must build or enhance the page header.
- `showcase.js` must initialize Preview / Code tabs.
- `showcase.js` must initialize Copy buttons.
- `showcase.css` must own all showcase layout, sidebar, tabs, code block, and responsive styling.
- Component showcases must not duplicate shell layout markup.

Validation:

- Shared showcase files exist.
- Each showcase references shared showcase files.
- Each showcase declares `data-current-component`.
- Each showcase declares `data-showcase-title`.
- Each showcase has `data-showcase-content`.
- Code examples contain only reusable component markup.
- Copied code is reusable outside the showcase.

### Showcase Generation Order

Preferred generation order:

1. Create shared showcase infrastructure if missing.
2. Generate component files.
3. Generate showcase examples.
4. Attach showcase to shared showcase infrastructure.

Rules:

- Never duplicate showcase infrastructure inside component showcases if shared infrastructure exists.
- Prefer updating `components/_showcase/showcase.css` and `components/_showcase/showcase.js` over creating new showcase-specific infrastructure.
- Component showcases should contain only component-specific examples and documentation.

### Showcase Asset Requirements

Every generated showcase must load the design system token file.

Required:

```html
<link rel="stylesheet" href="../../token.css" />
```

## Final Validation Checklist Before finishing generation verify: - Variant count matches manifest. - All template

classes exist in CSS. - All documented states exist in CSS. - All missing tokens are documented. - All deviations are
documented. - No primitive token leakage. - No hardcoded visual values. - No orphan selectors. - No orphan template
classes. - All visual-only interaction layers are converted to pseudo-elements. - No Interaction Circle / Ripple / Hover
Overlay exists as standalone HTML unless explicitly required. - Focus Ring is implemented with `:focus-visible`,
`::after`, or `outline`. - Interaction layers do not cover structural controls. - Z-index layering is documented and
validated. - State deltas are implemented as CSS selectors, not duplicated markup. ## Final Response Format Always end
with: ```text Done. Mode: - Analyze / Plan / Generate / Review Files created: - ... Files updated: - ... High severity
issues: - ... Medium severity issues: - ... Low severity issues: - ... Advisory: - ... Missing tokens: - ... Missing
standards: - ... Recommended next step: - ...

```

## Autonomous Generation

When generation is requested:

The skill must automatically execute:

1. Analyze
2. Plan
3. Generate
4. Review

without requiring separate user prompts.

If High severity issues are found:

- Stop.
- Report the issues.
- Do not continue.

If only Medium, Low, or Advisory issues exist:

- Apply safe fixes automatically.
- Re-run review.
- Produce final output.

The user should not need to manually request:

- analysis
- plan
- review
- fixes

unless explicitly desired.

## Default Behavior

If the user writes:

Generate [component-name]

The skill should automatically:

- analyze manifest
- create plan
- generate files
- review files
- fix safe issues
- return final report

without additional instructions.
```

## Reference Component Policy

The current component manifest is the only source of truth for component behavior, states, variants, anatomy, and visual decisions.

Other existing components may be read only as formatting references.

Allowed:

- Read another component to understand file structure.
- Read another component to match schema shape.
- Read another component to align documentation format.
- Read another component to understand naming conventions.

Not allowed:

- Do not copy visual values from another component.
- Do not copy tokens from another component.
- Do not copy states from another component.
- Do not copy accessibility behavior from another component unless it is explicitly required by the current manifest.
- Do not copy compliance mappings directly from another component.
- Do not infer missing behavior from button, chip, or any other component.

When generating a component, the skill must first use:
components/[component-name]/manifest.json

or the component-local JSON source provided by the user.

If another component is read, it must be treated as a format reference only, not as a source of component behavior.

- No behavior, states, tokens, or accessibility rules were copied from another component unless explicitly justified in analysis.md.

## Focus Policy

Do not assume :focus-visible by default.

Determine focus behavior from:

- Platform Code standards
- Accessibility standards
- Manifest analysis
- Focus layer geometry

Allowed implementations:

- :focus
- :focus-visible
- :focus-within

Document the chosen strategy in analysis.md.

If the source does not explicitly require keyboard-only focus behavior,
do not automatically prefer :focus-visible.
