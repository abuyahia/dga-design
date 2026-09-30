# Foundation Stabilization

## F02 — Breadcrumb variable depth

Status: RESOLVED
Date: 2026-09-12

The existing Breadcrumb now has one ordered-item renderer supporting 1..N levels,
configurable root data, escaped labels/URLs and one non-navigable current item.
Service Detail and Contact use it directly. Page Intro and Heavy Content retain
the two-level call through a builder compatibility adapter delegating to the same
renderer. The historical foundation audit is unchanged.

Files changed:

- `components/breadcrumb/{template,item,link,current,separator,two-level}.html`
- `components/breadcrumb/breadcrumb.contract.md`
- `scripts/breadcrumb_markup.py`
- `scripts/build_site.py`
- `scripts/service_markup.py`
- `scripts/contact_markup.py`
- `sections/contact/template.html`
- `templates/contact/contact.css`
- `templates/service/service.css`
- `tests/test_breadcrumb.py`
- `docs/component-registry.md`
- `docs/foundation-stabilization.md`

Validation:

- 5 focused Breadcrumb unit tests passed: 1/2/3/7 levels, ordered/current/link
  semantics, configurable root, label/attribute escaping, invalid destinations
  and hierarchy rejection, two-level compatibility, Page Intro, Service Detail
  and Contact integration.
- 6 existing focused tests passed: Page Intro variants/FAQ compatibility,
  Heavy Content build compatibility, Service Detail build destinations/escaping,
  and the 3 Contact rendering/data tests.
- Existing build tests wrote only to temporary directories.
- Shared Breadcrumb CSS and its RTL separator flip remain unchanged. Canonical
  separators replace the former Contact/Service asset arrows; redundant local
  breadcrumb styles were removed. Form layout and behavior were not changed.
- No browser/E2E suite or screenshot matrix was run; pixel equivalence of the old
  independent breadcrumbs is not asserted.

Scope: F02 only. Other audit findings remain open; no Page Intro migration or
broader shared CSS refactoring was performed.

## F01 — Page Intro adoption

Status: RESOLVED
Date: 2026-09-12

Migrated Contact, Heavy Content and Service Detail heading/breadcrumb areas to
`sections/page-intro/template.html`. None of the three requires an exceptional
parallel introduction. Existing variants are unchanged; no component or variant
was added. Service Detail intentionally keeps its adjacent launch CTA, tags,
service description and agreement link outside the title region. Heavy Content's
TOC/body and Contact's form/sidebar remain outside Page Intro. Home Hero and Error
State remain justified non-internal-intro structures.

Files changed for F01:

- `scripts/page_intro_markup.py`
- `scripts/contact_markup.py`, `scripts/content_markup.py`, `scripts/service_markup.py`
- `sections/contact/template.html`, `sections/heavy-content/template.html`, `sections/service-overview/template.html`
- `sections/page-intro/description-group.html`, `sections/page-intro/README.md`
- `templates/government/composition.css`
- `templates/contact/contact.css`, `templates/content/content.css`, `templates/service/service.css`
- `tests/test_page_intro_adoption.py`
- `docs/component-registry.md`, `docs/foundation-stabilization.md`

Removed the three independent h1/breadcrumb wrappers, Contact intro rules, Heavy
Content header/lead/overview rules and Service title typography. Shared Page Intro
rules now consume scoped presentation settings that preserve the existing token
sizes, colors, padding and gaps, including Heavy Content's mobile title sizing.
The original shared stylesheet location remains unchanged (F03 is not addressed).

Validation: 14 focused unit/build tests passed: 2 adoption checks, 5 Breadcrumb
checks, 3 Contact checks, and 4 existing Page Intro/FAQ, Heavy Content, Form and
Service Detail checks. Temporary builds verify one h1 within one Page Intro,
2/3-level breadcrumb hierarchy and one current item, escaped labels, omission of
empty optional slots, FAQ compact, Form featured/required note, and retained TOC
and sidebar markup. Existing About/News/Services also participate in the targeted
intro build assertions. No full repository tests, browser/E2E suite or screenshot
matrix ran. Visual preservation was reviewed statically; pixel equivalence is not
claimed. The historical audit and the dated F02 record are unchanged.

## F03 — Shared asset ownership

Status: RESOLVED
Date: 2026-09-12

Canonical ownership and intentional boundaries are recorded in
`docs/shared-asset-ownership.md`. Page Intro, FAQ, Contact CTA, Heavy Content block
presentation and TOC/tab/progress/file-selection behavior now have section/component
owners. No value/interaction redesign, journey engine or generic utility layer was
introduced. The dated audit/F01/F02 records are preserved.

Moved/extracted files:

- `sections/page-intro/page-intro.css` from government composition CSS.
- `sections/faq/faq.css` and `sections/faq/faq.js` from FAQ template assets;
  generated bootstrap now `sections/faq/faq.runtime.js`.
- `sections/contact-cta/contact-cta.css` and `sections/contact-cta/assets/contact.svg`;
  CTA no longer uses the government home-feature-icon helper.
- `sections/heavy-content/heavy-content.css` from content template block rules.
- `components/table-of-contents/table-of-contents.js` from content template runtime.
- `components/tab/tab.js`, `components/progress-indicator/progress-indicator.js`,
  `components/file-upload/file-upload.js` extracted from consumer runtimes.

Other changed files:

- `scripts/build_site.py`, `templates/government/page.html`, `templates/government/composition.css`.
- `templates/content/content.css`, `templates/contact/contact.js`, `templates/form/form.js`, `templates/service/service.js`.
- `sections/faq/template.html`, `sections/contact-cta/template.html`, `sections/heavy-content/template.html`, `sections/contact/upload.html`.
- `sections/page-intro/README.md`, `docs/component-registry.md`, `docs/shared-asset-ownership.md`, this status file.
- `tests/test_asset_ownership.py`, `tests/browser-ownership.mjs`, the TOC asset expectation in `tests/test_site_build.py`.

Intentionally retained: page grids/sticky/placement settings, government example
shell and home orchestration, catalogue URL/filter integration, service hash/steps
links, Form demo workflow, Contact validation/submission and F10 field CSS. These
boundaries are explicit rather than hidden dependencies of generic runtimes.

Loading: filtered deterministic CSS lists; component runtimes precede selected
Contact/Form/Service integration scripts. Section scripts include only once. Asset
copying is deduplicated. Contact CSS remains loaded on Form explicitly for unresolved
F10, and is no longer loaded on unrelated pages.

Validation: 11 focused unit/build tests passed (ownership, adoption, Contact and
existing FAQ/Page Intro, Heavy Content, Form and Service checks). 23 focused Chrome
checks passed at one desktop viewport: required assets/one h1 on eight affected
pages, FAQ toggle, CTA own icon styling, TOC current item/idempotent init, tab
controller reuse/RTL-LTR arrows/End/hash/steps link, progress next/previous/current
state and repeated init, upload repeated mount/type-size-empty rejection/selection/
removal/focus. No full repository suite, browser suite, E2E or screenshot matrix.
Temporary outputs only; no dist pages changed. F04/F05/F10 and P2 work were not
performed.

## F10 — Shared field presentation

Status: RESOLVED
Date: 2026-09-13

Form no longer depends on Contact CSS. Existing Label ownership supplies the
neutral `.label__required` marker; Text Input owns shrink behavior and the reusable
`text-input--label-semibold` label variant. Input Affix owns its connected-field
height/alignment/radius rule. File Upload owns responsive root/file-row sizing,
long-name wrapping and name/action distribution.

Files changed for F10:

- `components/text-input/text-input.css`, `template.html`, `text-input.contract.md`
- Existing `components/label/label.css` remains the canonical marker owner; its
  implementation did not require a change
- `components/input-affix/input-affix.css`, `input-affix.contract.md`
- `components/file-upload/file-upload.css`, `file-upload.contract.md`
- `sections/contact/input.html`
- `scripts/contact_markup.py`, `scripts/form_markup.py`, `scripts/build_site.py`
- `templates/contact/contact.css`, `templates/form/form.css`
- `tests/test_form_field_presentation.py`, `tests/browser-form-field-presentation.mjs`
- `tests/test_asset_ownership.py`; corrected the F03 FAQ runtime expectation in
  `tests/test_site_build.py`
- `docs/component-registry.md`, `docs/shared-asset-ownership.md`, this status file

Removed duplicate/local selectors: `.contact-required`, both template-owned
`.text-input__label` rules, both template-owned Text Input shrink rules, the Form
Affix sizing rule, and Contact's five File Upload/File Item width/wrapping/row
rules. Contact retains its page/form grid, note/actions/error summary/sidebar and
responsive composition. Form retains its page/grid, field rows, action layout,
support-message presentation and mobile composition. Validation rules, accepted
file policy, submission adapter and demo progression are unchanged.

Validation: 11 focused unit/build tests passed across F10 ownership/markup,
Contact data/rendering, asset ownership, Page Intro consumers, the existing Form
case and focused site build. A focused Chrome comparison at 430px passed for
Contact and Form: no overflow, every `label[for]` resolves, required markers remain
decorative/red, label typography remains 14px/600/20px, Affix geometry remains
38px inside the 40px field with stretch/zero radius, and File Upload remains
398px wide with wrapping names and spaced actions. The before/after computed
values matched; Form changed from loading Contact CSS to not loading it. No full
repository/browser/E2E suite or screenshot matrix ran. F04/F05 and P2 work were
not performed.

## F05 — Disabled Link contract

Status: RESOLVED
Date: 2026-09-13

Canonical disabled Link examples now omit `href`, retain explicit `role="link"`
and `aria-disabled="true"`, and remain outside the tab order by default. The
documented focusability policy permits `tabindex="0"` only when intentional
focus discovery is required. Active Link examples and behavior are unchanged.

The Link template, showcase, component contract, CSS guidance, audit rules,
compliance mapping and registry now follow the same markup contract. The shared
core JavaScript activation guard remains unchanged as a defensive enhancement;
it is not the primary navigation-prevention mechanism.

Validation: canonical and showcase disabled examples were checked for absent
`href`, correct semantics, supported focus policy and intact disabled classes;
active example destinations were checked against the pre-change source. Link
JSON documents parsed successfully, 15 focused audit unit tests passed, and all
9 Link browser checks passed. The existing broader Core browser run passed 43
of 49 checks; its six failures were confined to the unchanged Accordion
keyboard/isolation assertion across direction and viewport combinations. No
full repository/browser/E2E suite or screenshot matrix ran. F04 and P2 work were
not performed.

## F04 — Documentation reconciliation

Status: RESOLVED
Date: 2026-09-13

The registry, Foundation guide, inventory and current component contracts now
describe the stabilized implementation. Local IBM Plex Sans Arabic assets and
their build loading are documented. Card documentation recognizes the registered
token surface and optional Avatar/media composition. Inventory records point to
15 implemented shell/section capabilities formerly marked `planned`, while retaining conservative
`needs_improvement`, `production_ready: false` and historical audit statuses.

Historical records remain historical: `docs/foundation-audit.md` is unchanged,
component audit rules keep their authored `not_run` states, and earlier validation
counts were not promoted into current certification evidence. F04 validation was
limited to JSON parsing, registered-path checks, contradictory-claim searches and
`git diff --check`; no implementation or browser/E2E work was performed.

## Foundation v1.0

Status: STABILIZED
Date: 2026-09-13

F01, F02, F03, F04, F05 and F10 are resolved. The historical Foundation audit
found no P0 blocker, and no P1 finding remains unresolved. Foundation v1.0 means
the shared tokens/Base, government shell, current shared components and sections,
asset ownership, Page Intro/Breadcrumb architecture, field-presentation ownership
and documented contracts are stable enough for product development.

This status does not qualify every reference component for production, implement
every P2 capability, provide whole-site search or a reusable semantic table,
certify formal accessibility or the full browser/E2E matrix, complete sector
products, or turn the experimental Form workflow into a production transaction
engine.

Deferred after v1.0:

- F06 — FAQ heading flexibility
- F07 — legacy path clarity
- F08 — core mounting outside FAQ
- F09 — configurable routes/content limits
- F11 — heavy-content media
- F12 — reusable table
- F13 — general site search/results
