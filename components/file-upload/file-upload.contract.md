# File Upload Contract

## Component Type

Composite

---

## Dependencies

Required:
- `_File` (`.file-item`) — file row indicator sub-component, consumed by Single (Uploaded state) and Multiple
- `_Drop Zone` (`.drop-zone`) — drag-and-drop area sub-component, consumed by Multiple

Optional:
- None

---

## Sub-Components

### `.file-item` — File Item

**States**: `loading`, `uploaded`, `error`

| State    | Modifier Class         | Description                                 |
|----------|------------------------|---------------------------------------------|
| loading  | (none)                 | Shows CSS spinner icon + filename + remove  |
| uploaded | (none)                 | Shows feedback icon + filename + remove     |
| error    | `.file-item--error`    | Error border + error message row visible    |

**Anatomy:**

| Element                    | Required | Description                            |
|----------------------------|----------|----------------------------------------|
| `.file-item`               | Yes      | Root element                           |
| `.file-item__row`          | Yes      | Main content row                       |
| `.file-item__lead`         | Yes      | Icon + filename wrapper                |
| `.file-item__icon`         | Yes      | 20×20 state indicator (spinner or SVG) |
| `.file-item__name`         | Yes      | Filename text                          |
| `.file-item__trail`        | Yes      | Remove button wrapper                  |
| `.file-item__remove`       | Yes      | Remove button (×)                      |
| `.file-item__error-row`    | No       | Error message row (Error state only)   |
| `.file-item__error-text`   | No       | Error message text                     |

**Required ARIA:**

```html
<div class="file-item" role="listitem">
  ...
  <button type="button" class="file-item__remove" aria-label="Remove [filename]">
    ...
  </button>
  ...
  <div class="file-item__error-row" role="alert">...</div>
</div>
```

---

### `.drop-zone` — Drop Zone

**States**: `default`, `drag-hover`, `disabled`

| State      | Modifier                 | Description                                          |
|------------|--------------------------|------------------------------------------------------|
| default    | (none)                   | Dashed border, neutral background                   |
| drag-hover | `.is-drag-hover`         | Success border/bg, text turns green, button disabled |
| disabled   | `[aria-disabled="true"]` | Disabled border, no bg, icon faded, button disabled  |

**Anatomy:**

| Element                | Required | Description                |
|------------------------|----------|----------------------------|
| `.drop-zone`           | Yes      | Root element               |
| `.drop-zone__icon`     | Yes      | 24×24 upload SVG icon      |
| `.drop-zone__text`     | Yes      | Text wrapper               |
| `.drop-zone__lead`     | Yes      | Lead text ("Drag and drop…") |
| `.drop-zone__helper`   | Yes      | Helper / constraints text  |
| `.drop-zone__trigger`  | Yes      | "Browse Files" button      |

**Required ARIA:**

```html
<div class="drop-zone" role="region" aria-label="File drop zone">
  ...
  <button type="button" class="drop-zone__trigger">Browse Files</button>
</div>
```

---

### `.file-upload` — Single File Upload

**States**: `default`, `disabled`, `uploaded`

| State    | Modifier                 | Description                       |
|----------|--------------------------|-----------------------------------|
| default  | (none)                   | Label + helper + trigger button   |
| disabled | `[aria-disabled="true"]` | All elements appear disabled      |
| uploaded | `.is-uploaded`           | File item appears below trigger   |

**Anatomy:**

| Element                   | Required | Description                    |
|---------------------------|----------|--------------------------------|
| `.file-upload`            | Yes      | Root element                   |
| `.file-upload__header`    | Yes      | Label + helper wrapper         |
| `.file-upload__label-row` | Yes      | Label alignment row            |
| `.file-upload__label`     | Yes      | Visible label text             |
| `.file-upload__helper`    | No       | Helper / constraints text      |
| `.file-upload__trigger`   | Yes      | "Browse Files" button          |
| `.file-upload__file`      | No       | Container for `.file-item` (shown in Uploaded state) |

**Required ARIA:**

```html
<div class="file-upload" aria-disabled="true|false">
  <div class="file-upload__header">
    <div class="file-upload__label-row">
      <label class="file-upload__label" for="[input-id]">Upload files</label>
    </div>
    <p class="file-upload__helper">...</p>
  </div>
  <input type="file" id="[input-id]" hidden aria-hidden="true" tabindex="-1">
  <button type="button" class="file-upload__trigger">Browse Files</button>
  <div class="file-upload__file" aria-live="polite">
    <!-- .file-item injected here -->
  </div>
</div>
```

---

### `.file-upload--multiple` — Multiple File Upload

**States**: `default` only (states delegated to `.drop-zone` and `.file-item`)

**Anatomy:**

| Element                  | Required | Description                    |
|--------------------------|----------|--------------------------------|
| `.file-upload--multiple` | Yes      | Root element                   |
| `.drop-zone`             | Yes      | Drop zone instance             |
| `.file-upload__files`    | No       | File list container            |

**Required ARIA:**

```html
<div class="file-upload--multiple">
  <div class="drop-zone" role="region" aria-label="File drop zone">...</div>
  <div class="file-upload__files" role="list" aria-label="Uploaded files">
    <!-- .file-item × N -->
  </div>
</div>
```

---

## RTL Support

RTL is handled via `dir="rtl"` on an ancestor element (or the component root).

- Single: header alignment flips to `flex-end`; label and helper text align right
- File Item: Trail wrapper (remove button) moves to start; text aligns right
- Drop Zone: no CSS change needed (centered symmetric layout)

---

## CSS Custom Properties

All properties are component-scoped and fallback to manifest source tokens.

```css
/* File Item */
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

/* Drop Zone */
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

/* Single file upload */
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
```

> All tokens are missing from `token.css` — see `analysis.md` Missing Tokens section.
