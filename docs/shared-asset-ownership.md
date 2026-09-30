# Shared asset ownership — F03

The builder copies canonical source assets once and renders deterministic ordered
CSS/script lists. Component scripts below load before the consuming integration.
Classic-script APIs match the existing file-preview build; none requires a framework.

| Owner | Reusable asset | Consumer boundary |
|---|---|---|
| Page Intro | `sections/page-intro/page-intro.css` | Template CSS keeps embedded intro token settings and grid/flex placement. Existing five variants unchanged. |
| FAQ section | `sections/faq/faq.css`, `sections/faq/faq.js` | Builder combines core source and FAQ bootstrap as `sections/faq/faq.runtime.js`; section includes it once. No FAQ-only layout CSS remains. |
| Contact CTA | `sections/contact-cta/contact-cta.css`, `assets/contact.svg` | Card/Button remain independent dependencies. The small icon wrapper belongs to this CTA, not a government helper or an icon system. |
| Heavy Content | `sections/heavy-content/heavy-content.css` | Body blocks, headings, lists and media presentation are section-owned. Outer grid, TOC column/stickiness, page padding, intro settings and divider placement stay in `templates/content/content.css`. |
| Table of Contents | `components/table-of-contents/table-of-contents.js` | Same fragment/click/scroll behavior and 160px active threshold; includes native-link fallback. `PlatformTableOfContents.init(scope)` auto-runs once and skips mounted roots on subsequent calls. |
| Tab | `components/tab/tab.js` | Generic **horizontal** ARIA roles, panel visibility, roving tabindex, RTL/LTR arrows and Home/End. Service hash updates, hash restoration, steps link and redundant panel heading suppression remain in `templates/service/service.js`. No new vertical-tab behavior is claimed. |
| Progress Indicator | `components/progress-indicator/progress-indicator.js` | Current/completed classes, one aria-current step and mobile summary update. Next/previous buttons, status text and current workflow state stay in Form. |
| File Upload | `components/file-upload/file-upload.js` | Single-file browse/name/removal/focus and visual error state. Contact owns accepted formats, size/empty-file rules, field errors, pending/disabled orchestration, reset and submission. No backend functionality. |

## Runtime contracts

- `PlatformTabs.mount(root, {onSelect(panel, index)})` returns `{select, panels}`.
  Root contains `.tab-list` buttons with unique IDs and `data-panel` pointing to
  child panel IDs. `select(index, focus=false)` changes presentation without route
  side effects; user activation calls onSelect. The API enhances the existing
  horizontal tab contract; callers supply valid indexes and unique panel IDs.
- `PlatformProgressIndicator.mount(root)` returns `{update}`. Root uses the existing
  `[data-progress-indicator]` fragment/hooks. `update(step)` clamps to available
  steps and returns `{current, total, title}` for consumer announcements.
- `PlatformFileUpload.mount(root, {validate(file), onError(message)})` returns
  `{clear}`. Single-file root contains `input[type=file]`, `[data-file-browse]`,
  `[data-file-remove]`, `[data-file-name]` and `.file-item`. Contact's old data hooks
  remain compatibility aliases for its own error-summary focus and existing tests.
  Validators return an empty string for no error. Consumer owns submission/reset
  policy and explicitly calls clear after successful reset, as before.
- Mount APIs return the same controller for an already mounted root. The first
  mount owns callbacks; consumers must not remount to change callback configuration.
  They attach listeners once and do not provide a new teardown/SPA lifecycle API.

## Intentionally retained template ownership

- Government composition/home script: the example shell's service-search dialog,
  configured home carousel/hero orchestration, home statistics/news geometry and
  `.section-heading`/home layout helpers remain composition-level contracts, not
  a newly promised standalone generic section library. Their current hardcoded
  routes/content limits are outside this task. CTA no longer borrows their icon.
- Service catalogue: query/audience URL state, Arabic normalization/results copy,
  specific filter/card selectors and catalogue page grid remain the cohesive
  service-page integration. This is not a generic search runtime; extracting it
  for symmetry would broaden the contract. Generic tab interaction is extracted.
- Service/Contact/Form page grids, sidebars, spacing and Error illustrations remain
  template-owned. Form demo navigation is not a reusable journey engine.
- Field ownership was stabilized by F10: Label owns `.label__required`, Text Input
  owns its semibold-label modifier and shrink behavior, Input Affix owns connected
  sizing, and File Upload owns responsive file rows/name wrapping. Contact CSS is
  selected only for Contact. Form keeps only its grid, support and action layout.

## Loading

`STYLE_SECTIONS` and `page_styles` filter the established ordered asset list for
owned sections/template styles. `page_scripts` selects Contact/Form/Service scripts
and inserts their component dependencies first. FAQ and Heavy Content already
include their scripts through their section fragments; no second include is added.
Global shell/core component CSS order is otherwise preserved. The build deduplicates
copy destinations; source-only support files are not duplicate browser inclusions.

The removed old FAQ/Content asset paths are no longer live build dependencies.
Rebuild exported pages when consuming this change; old generated output should not
be mixed with new assets. No generated `dist/` files were modified by this task.
