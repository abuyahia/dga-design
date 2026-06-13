# Component Analysis

- Manifest paths: `mainifest-single.json`, `mainifest-drop_zone.json`, `mainifest-file.json`, `mainifest-multiple.json`
- Component name: File Upload (Single, Multiple, Drop Zone, File Item)

---

## Source

Four Figma COMPONENT_SET exports in one folder:

| Set name              | File                       | Variants |
|-----------------------|----------------------------|----------|
| File Upload / Single  | mainifest-single.json      | 6        |
| _Drop Zone            | mainifest-drop_zone.json   | 6        |
| _File                 | mainifest-file.json        | 6        |
| File Upload / Multiple| mainifest-multiple.json    | 2        |

---

## Detected Anatomy

### File Upload / Single

```
.file-upload
├── .file-upload__header
│   ├── .file-upload__label-row
│   │   └── .file-upload__label (label text)
│   └── .file-upload__helper (helper text)
├── .file-upload__trigger (button — Browse Files)
└── .file-upload__file (optional — visible in Uploaded state)
    └── .file-item (see below)
```

### _Drop Zone

```
.drop-zone
├── .drop-zone__icon (SVG 24×24 — file-upload icon)
├── .drop-zone__text
│   ├── .drop-zone__lead (Lead Text)
│   └── .drop-zone__helper (Helper Text)
└── .drop-zone__trigger (button — Browse Files)
```

### _File (File Item)

```
.file-item
├── .file-item__row
│   ├── .file-item__lead
│   │   ├── .file-item__icon (Feedback Icon or Loading spinner)
│   │   └── .file-item__name (File Name)
│   └── .file-item__trail
│       └── .file-item__remove (button — × close)
└── .file-item__error-row (visible in Error state only)
    └── .file-item__error-text
```

### File Upload / Multiple

```
.file-upload--multiple
├── .drop-zone (instance)
└── .file-upload__files (list)
    └── .file-item × N
```

---

## Detected Axes

| Axis                | Values                              | CSS Mechanism                          |
|---------------------|-------------------------------------|----------------------------------------|
| type                | single, multiple                    | `.file-upload` / `.file-upload--multiple` |
| state (single)      | default, disabled, uploaded         | `[aria-disabled]`, `.is-uploaded`      |
| state (drop-zone)   | default, drag-hover, disabled       | `.is-drag-hover`, `[aria-disabled]`    |
| state (file-item)   | loading, uploaded, error            | `.is-loading`, class on root           |
| rtl                 | false, true                         | `[dir=rtl]` selectors                  |

---

## Detected Variants

**Single** (6): RTL=False/True × State=Default/Disabled/Uploaded

**Drop Zone** (6): State=Default/Drag+hover/Disabled × RTL=False/True

**File Item** (6): State=Loading/Uploaded/Error × RTL=False/True

**Multiple** (2): RTL=no / RTL=yes

---

## Detected States

- Single: `default`, `disabled`, `uploaded`
- Drop Zone: `default`, `drag-hover`, `disabled`
- File Item: `loading`, `uploaded`, `error`

---

## Detected Sizes

No size axis. All dimensions are fixed from manifest tokens:
- Button height: 32px
- Drop zone padding: 24px
- File item padding: 8px

---

## Architecture Findings

1. Four component sets are treated as one package. `_File` and `_Drop Zone` are sub-components consumed by Single and Multiple.
2. The Button instances inside these components are inline — their tokens are borrowed from Button namespace.
3. RTL for Drop Zone is symmetric (centered layout) — no separate CSS class needed. Handled via `[dir=rtl]` on ancestor and `dir` attribute.
4. RTL for Single: header alignment flips from `flex-start` to `flex-end`. Handled via `[dir=rtl]`.
5. RTL for File Item: Trail wrapper and Text wrapper swap order in RTL. Handled via `[dir=rtl]` flex-direction reversal.
6. Loading spinner (two ELLIPSE shapes in Figma) is implemented as a CSS `@keyframes` border spinner — avoids SVG complexity while matching visual intent.
7. `Feedback Icon` is a 20×20 instance. In Uploaded = success checkmark. In Error = error icon. Represented as inline SVG in template (TODO: source from icon library).
8. `Button-Close` is rendered as `<button type="button">` following semantic HTML requirements.
9. The hidden `<input type="file">` is implied by browser file selection — not in Figma but required in HTML.
10. Drop zone drag-hover state requires JS toggling `.is-drag-hover` class on dragover/dragleave/drop events.

---

## Token Findings

All component-level tokens are proposed and missing from `token.css`. Mapped from manifest source tokens:

| Manifest token                          | Component token                        |
|-----------------------------------------|----------------------------------------|
| `--Form-field-text-label`               | `--file-upload-label-color`            |
| `--Global-text-default-disabled`        | `--file-upload-label-disabled-color`   |
| `--text-text-tertiary`                  | `--file-upload-helper-color`           |
| `--Global-text-default-disabled`        | `--file-upload-helper-disabled-color`  |
| `--Button-button-background-black-default` | `--file-upload-trigger-bg`          |
| `--Global-background-disabled`          | `--file-upload-trigger-bg-disabled`    |
| `--Text-text-oncolor-primary`           | `--file-upload-trigger-text-color`     |
| `--Border-border-neutral-primary`       | `--drop-zone-border` / `--file-item-border` |
| `--Background-background-neutral-100`   | `--drop-zone-bg` / `--file-item-bg`    |
| `--Border-border-success`               | `--drop-zone-border-draghover`         |
| `--Background-background-success-25`    | `--drop-zone-bg-draghover`             |
| `--Text-text-success`                   | `--drop-zone-lead/helper-color-draghover` |
| `--Global-border-disabled`              | `--drop-zone-border-disabled`          |
| `--Text-text-display`                   | `--drop-zone-lead-color`               |
| `--Text-text-primary-paragraph`         | `--drop-zone-helper-color`             |
| `--Border-border-error`                 | `--file-item-border-error`             |
| `--text-text-error-primary`             | `--file-item-error-text-color`         |
| `--Button-button-background-neutral-default` | `--drop-zone-trigger-bg`         |

---

## Accessibility Findings

1. Browse Files button: `<button type="button">` triggers hidden `<input type="file">`.
2. Hidden file input: `<input type="file" hidden aria-hidden="true" tabindex="-1">`.
3. Drop zone: `role="region"` + `aria-label="File drop zone"`.
4. Drag-hover state: `aria-live="polite"` region for screen reader announcement.
5. File item remove button: `aria-label="Remove [filename]"` required.
6. File item loading: `role="status"` with descriptive label.
7. File item error: error text associated via `aria-describedby`.
8. Disabled state: `aria-disabled="true"` on root + `disabled` on button.
9. Focus: `:focus-visible` on all interactive elements.

---

## Compliance Findings

- No officially compliant mappings in place.
- `official_compliance_claim: false`
- `overall_status: pending_audit`

---

## Implementation Decisions

1. Single CSS file covers all sub-components: `.drop-zone`, `.file-item`, `.file-upload`, `.file-upload--multiple`.
2. RTL handled via `[dir=rtl]` attribute selectors — no separate modifier class.
3. Loading spinner: pure CSS `@keyframes rotate` on `.file-item__icon` — no JS dependency.
4. Drop zone drag interaction: JS toggling `.is-drag-hover` class only. All styles in CSS.
5. Single Browse Files button: dark/black background (primary action in content-light context).
6. Drop Zone Browse Files button: neutral background (secondary action in visually heavy zone).
7. File items in Multiple share the same `.file-item` CSS as Single's uploaded file item.

---

## Intentional Deviations From Figma

1. **Loading icon**: Figma shows two ELLIPSE SVG shapes (Track + Tail). Implemented as CSS border spinner — matches visual intent without inline SVG complexity.
2. **Feedback Icon**: Figma uses a component instance. Template uses inline SVG placeholder — TODO for production icon sourcing.
3. **Drop Zone RTL**: No CSS class needed — layout is centered/symmetric. Handled by `dir` attribute.
4. **Button-Close**: Rendered as semantic `<button>` instead of Figma `INSTANCE` frame.
5. **Hidden input**: Added `<input type="file" hidden>` — present in HTML only, not Figma.

---

## Risks

1. Component-level token names unvalidated against actual `token.css`.
2. Loading spinner CSS may need fine-tuning for exact fidelity.
3. Feedback Icon SVG content requires sourcing from icon library.
4. Drag-and-drop JS is application-layer responsibility — not provided.

---

## Assumptions

1. `Feedback Icon` in Uploaded state = success checkmark (green).
2. `Feedback Icon` in Error state = error/warning icon (red).
3. `Loading` instance = circular spinner animation.
4. `Button-Close` triggers file removal in all states.
5. Multiple mode allows unbounded file list.
6. Single mode: Browse replaces the selected file; Uploaded state shows the one selected file.
7. Drop zone Browse Files in drag-hover state appears disabled to communicate "drop here instead."

---

## Known Issues

1. All component-level token names are proposed — not yet in `token.css`.
2. No drag-and-drop JS provided.
3. Feedback Icon SVG is placeholder.

---

## Missing Tokens

```
--file-upload-label-color
--file-upload-label-disabled-color
--file-upload-helper-color
--file-upload-helper-disabled-color
--file-upload-gap
--file-upload-trigger-bg
--file-upload-trigger-bg-disabled
--file-upload-trigger-text-color
--file-upload-trigger-text-disabled-color
--file-upload-trigger-height
--file-upload-trigger-padding-x
--file-upload-trigger-gap
--file-upload-trigger-radius
--file-upload-trigger-font-size
--file-upload-trigger-font-weight
--file-upload-trigger-line-height
--drop-zone-border
--drop-zone-border-draghover
--drop-zone-border-disabled
--drop-zone-bg
--drop-zone-bg-draghover
--drop-zone-lead-color
--drop-zone-lead-color-draghover
--drop-zone-lead-color-disabled
--drop-zone-helper-color
--drop-zone-helper-color-draghover
--drop-zone-helper-color-disabled
--drop-zone-icon-opacity-disabled
--drop-zone-radius
--drop-zone-padding
--drop-zone-gap
--drop-zone-trigger-bg
--drop-zone-trigger-bg-draghover
--drop-zone-trigger-text-color
--drop-zone-trigger-text-disabled-color
--drop-zone-trigger-height
--drop-zone-trigger-padding-x
--drop-zone-trigger-radius
--file-item-border
--file-item-border-error
--file-item-bg
--file-item-radius
--file-item-padding
--file-item-gap
--file-item-name-color
--file-item-name-font-size
--file-item-name-font-weight
--file-item-name-line-height
--file-item-error-text-color
--file-item-error-separator
--file-item-remove-size
--file-item-remove-radius
--file-item-icon-size
```

---

## Missing Standards

- Platform Code file-upload WCAG 2.2 AA mapping: pending
- Platform Code keyboard interaction spec: pending

---

## TODO

- [ ] Validate all component-level token names against `token.css`
- [ ] Source Feedback Icon SVGs (success, error) from icon library
- [ ] Implement drag-and-drop JS in application layer
- [ ] Add ARIA live region for drag-hover state announcement
- [ ] Update `token.css` with all missing component-level tokens
- [ ] Add `file-upload` to `components/_showcase/showcase.js` COMPONENTS registry

---

## Component Classification

**Package classification**: Composite

The file-upload package contains:
- `_File` → Primitive (self-contained file row)
- `_Drop Zone` → Primitive (self-contained drop zone)
- `File Upload / Single` → Composite (uses _File + inline Button)
- `File Upload / Multiple` → Composite (uses _Drop Zone + _File instances)

---

## Component Dependencies

Required:
- `_Drop Zone` — consumed by `File Upload / Multiple`
- `_File` — consumed by `File Upload / Single` (Uploaded state) and `File Upload / Multiple`

Optional:
- None

---

## Dependency Confirmation

Proceeding without explicit dependency confirmation — "Generate file-upload" treated as implicit approval. All assumptions documented above.

---

## Layer Classification

| Layer            | Figma Type | Implementation Role | HTML Strategy      |
|------------------|------------|---------------------|--------------------|
| Drop zone area   | FRAME      | Structural          | `<div class="drop-zone">` |
| file-upload icon | INSTANCE   | Icon                | Inline SVG         |
| Lead Text        | TEXT       | Structural          | `<p>`              |
| Helper Text      | TEXT       | Structural          | `<p>`              |
| Button (trigger) | INSTANCE   | Structural          | `<button>`         |
| Feedback Icon    | INSTANCE   | Icon                | Inline SVG         |
| Loading          | INSTANCE   | Icon (animation)    | CSS border-spinner |
| Button-Close (×) | INSTANCE   | Structural          | `<button>`         |
| Error message    | FRAME/TEXT | Structural          | `<div>`            |

No Interaction Circle, Ripple, Hover Overlay, or Focus Ring layers detected in any manifest.

---

## State Delta Matrix

### File Upload / Single

| Delta             | Default      | Disabled             | Uploaded             |
|-------------------|--------------|----------------------|----------------------|
| Label color       | label-token  | disabled-token       | label-token          |
| Helper color      | tertiary     | disabled             | tertiary             |
| Trigger bg        | black        | bg-disabled          | black                |
| Trigger text      | white        | disabled             | white                |
| File item visible | `display:none` | `display:none`    | `display:flex`       |
| Cursor            | auto         | not-allowed          | auto                 |

### _Drop Zone

| Delta          | Default           | Drag+hover          | Disabled             |
|----------------|-------------------|---------------------|----------------------|
| Border         | 1px dashed neutral| 2px dashed success  | 1px dashed disabled  |
| Background     | neutral-100       | success-25          | none                 |
| Lead color     | text-display      | text-success        | disabled             |
| Helper color   | text-paragraph    | text-success        | disabled             |
| Icon opacity   | 1                 | 1                   | 0.7                  |
| Trigger bg     | neutral           | bg-disabled         | bg-disabled          |
| Trigger text   | default           | disabled            | disabled             |

### _File (File Item)

| Delta         | Loading       | Uploaded          | Error              |
|---------------|---------------|-------------------|--------------------|
| Border        | neutral solid | neutral solid     | error solid        |
| Icon type     | CSS spinner   | success checkmark | error icon         |
| Error row     | hidden        | hidden            | visible            |

---

## Pseudo-Element Decisions

No Interaction Circle, ripple, or overlay layers detected in any manifest.
No pseudo-elements required from layer analysis.

Focus implemented via `:focus-visible` with `outline` on:
- `.file-upload__trigger:focus-visible`
- `.drop-zone__trigger:focus-visible`
- `.file-item__remove:focus-visible`

---

## Interaction Layer Decisions

No interaction layers found. Drag-hover uses CSS class `.is-drag-hover` toggled by application JS.

---

## Focus Layer Decisions

No Focus Ring layers detected. Focus strategy: `:focus-visible` with `outline` on all interactive elements. Chosen because the interactive targets (buttons) support both mouse and keyboard; `:focus-visible` ensures focus rings appear for keyboard users only per browser heuristics.

---

## Z-Index / Layering Decisions

No overlapping layers. No z-index required.

---

## Severity Classification

High: None

Medium:
- All component-level tokens are proposed names not yet validated against `token.css`

Low:
- Feedback Icon SVG content is placeholder

Advisory:
- CSS loading spinner is an approximation of Figma two-ellipse design
- Drag-and-drop JS is application-layer responsibility

---

## Assembly Awareness

```
_File ─────────┐
               ├── File Upload / Single
               │
_Drop Zone ────┤
               └── File Upload / Multiple
                         │
                         └── form-field → form
```

Component CSS is scoped to `.file-upload`, `.drop-zone`, `.file-item` — does not leak into parent structures.
