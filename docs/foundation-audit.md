# DGA Foundation Audit

## Executive Summary

**Overall status: NEEDS FIX — suitable for continued product prototyping, not yet a stabilized Foundation v1.0 release.** No verified P0 blocker prevents future product development. The main release concerns are incomplete Page Intro adoption, parallel breadcrumb assembly, shared styling owned by templates, and documentation/examples that no longer match the implementation.

Audit date: 2026-09-12. Scope: current local implementation, beginning with `AGENTS.md` and `docs/component-registry.md`, then the build path, its components, sections, template styles and relevant existing validation records. This is an architecture and static implementation audit, not a fresh DGA/Figma conformity assessment or accessibility certification.

Only this report was created. No implementation, registry, CSS, assets or existing pages were modified. No browser, E2E or screenshot suite was run. One existing Page Intro unit test passed; it builds into a temporary directory.

**Counting convention:** the 25 uniquely identified assessment items below are the sole counting source. Component and template tables are coverage views referencing those items, not additional findings. READY items have no issue severity.

| Status | Unique assessment items |
|---|---:|
| READY | 12 |
| NEEDS FIX | 8 |
| DUPLICATE | 3 |
| MISSING | 2 |
| Total | 25 |

| Issue severity | Count |
|---|---:|
| P0 — blocks future product development | 0 |
| P1 — should be fixed before Foundation v1.0 | 6 |
| P2 — useful improvement, can wait | 7 |
| P3 — optional/cosmetic | 0 |

EXPERIMENTAL is used only in the template coverage table for the intentionally demonstrative form. It is not counted as an extra issue.

## Foundation Status

READY means the inspected scope has a usable shared implementation with no material defect established here. It does not certify every variant, viewport or interaction. NEEDS FIX includes verified maintainability and contract inconsistencies; it does not necessarily mean the current page renders incorrectly. DUPLICATE distinguishes parallel ownership from legitimate composition. MISSING means a bounded foundation capability is absent, not that a sector-specific page must be built.

### Verified strengths

| Item | Status | Severity | Evidence — FACT | Recommendation |
|---|---|---|---|---|
| R01 — Central design tokens | READY | — | `token.css` contains primitives, semantic aliases and component tokens, including `--card-width` and `--card-padding`; component CSS consumes them. `standards/foundation-policy.json` records the audit policy. | Preserve the token system; no replacement or new parallel scale is needed. |
| R02 — Base and typography | READY | — | `styles/base/global.css` provides a low-specificity reset, native-control font inheritance, responsive media and opt-in `.ds-prose`. `assets/fonts/fonts.css` defines local Arabic font weights 400/500/600/700, included by `scripts/build_site.py:ASSETS`. | Retain opt-in editorial typography and the explicit font asset dependency. |
| R03 — Spacing, containers and layout utilities | READY | — | `styles/base/layout.css` provides container, reading width, stack, cluster and grid; uses logical padding and 768/1280 breakpoints with shrinking grid tracks. | Reuse these helpers; a utility framework or 12-column rewrite is unnecessary. |
| R04 — Global accessibility foundation | READY | — | `styles/base/accessibility.css` owns visually hidden text, skip-link focus, fallback focus rings and reduced motion. `templates/government/page.html` provides a focusable main target and viewport metadata. | Preserve these assets in every consuming shell; verify component-specific overrides when changes occur. |
| R05 — Navigation Header | READY | — | `partials/site-header/template.html` and navigation item fragments compose one header. `components/navigation-header/navigation-header.js` handles disclosure, Escape, focus return, responsive state and cleanup; navigation comes from configuration. | Keep this canonical component. General search ownership is separately covered by F03/F13. |
| R06 — Footer | READY | — | `partials/site-footer/template.html` wraps `scripts/footer_markup.py` output from `components/footer/` fragments and centralized `footer.css`; footer groups are supplied by the builder. | Retain the renderer and component CSS; route assumptions are covered by F09. |
| R07 — Digital Stamp | READY | — | `components/digital-stamp/template.html`, `scripts/digital_stamp_markup.py` and component CSS/JS provide configured preview/registered modes. Native details owns disclosure; JS adds Escape and cleanup. | Preserve preview versus registered semantics and the shared placement. |
| R08 — Button and enabled Link primitives | READY | — | Component CSS is centralized in `components/button/button.css` and `components/link/link.css`; live sections use native anchors/buttons. `scripts/core/index.js` documents and supplies enhanced disabled guards. | Reuse native semantics. Disabled Link examples are a separate exception, F05. |
| R09 — Native field building blocks | READY | — | Text Input, Label, Checkbox, Radio, Select and Textarea have component CSS and native input/label markup; contact/form renderers associate labels and error descriptions. Core handles mixed/readonly checkbox enhancement. | Retain these primitives. Composite field ownership needs F10; this is not approval of every historic showcase state. |
| R10 — Static content primitives | READY | — | Divider, List and Table of Contents have centralized CSS. Heavy content uses the breadcrumb and TOC fragments, List classes, semantic headings and fragment links. TOC uses `aria-current="location"`. | Reuse existing contracts; TOC runtime placement is F03. Divider and List reference HTML being examples is not itself duplication. |
| R11 — Page Feedback / Service Rating | READY | — | `scripts/feedback_markup.py`, `sections/feedback/template.html`, both feedback component packages and `styles/composites/feedback.js` share composition and state logic. Explicit submit adapters distinguish local preview from confirmed submission. | Keep the adapter boundary. Backend implementation is product integration, not a missing foundation component. |
| R12 — Page Intro slot and variant implementation | READY | — | `sections/page-intro/template.html` and `scripts/page_intro_markup.py` implement the five requested slots and all five variant names; the existing targeted test passed. | Keep this contract; adoption and stylesheet ownership are F01/F03. |

## Core / Base Audit

R01–R04 cover tokens, base CSS, typography, spacing, containers, layout, responsive foundations, RTL foundations and global utilities. No evidence justifies replacing these layers.

**FACT:** templates also load `templates/government/tokens.css`, which contains home-specific geometry and an overlay color. These values are not an alternative global token system. Similarly, numeric geometry such as the heavy-content sidebar width is not automatically an invalid token omission; its reference and semantic role matter.

**FACT:** existing `docs/batch-2-result.json` records a past strict audit and targeted browser work. It is historical evidence, not a test rerun in this audit. The current full token graph was not re-certified.

Documentation drift affecting this layer is F04. Shared field styles crossing template boundaries are F10.

## Components Audit

The primary registry is incremental, so inspection also followed components explicitly loaded by `scripts/build_site.py`. “Template dependency” below concerns extraction/reuse, not a claim of current browser failure.

| Component / relevant scope | Status | Evidence and reuse assessment | Action / finding |
|---|---|---|---|
| Navigation Header | READY | Shared data-generated links and responsive disclosure; component CSS and JS. Native navigation, buttons and ARIA states. | R05; keep canonical implementation. |
| Footer | READY | Shared fragment renderer and scoped CSS, with existing RTL/LTR result records. | R06; configurable shell routes need F09. |
| Digital Stamp | READY | Native disclosure, registered/preview data validation and dedicated runtime. | R07. |
| Breadcrumb | DUPLICATE | Two-level fragment is reusable and wrapping/logical CSS exists; service and contact construct additional markup paths. | F02; extend the existing component for variable depth. |
| Button / active Link | READY | Native elements with token-based centralized styles; no independent template button stylesheet was found. | R08. |
| Disabled Link reference examples | NEEDS FIX | Examples retain live hrefs despite the newer executive contract requiring removal. | F05. |
| Card | NEEDS FIX | Shared surface/content/actions CSS is reused by news, services, CTA and sidebars. Contract still mandates an always-present Avatar and says tokens are missing, contrary to implementation. | F04. Static cards remain useful; expandable/selectable behavior is consumer-owned, not a certified shared runtime. |
| Service Card | READY | `components/service-card/template.html` composes Card, tags and Button anchors; the same `service_card()` renders home, catalogue and related services. Component CSS is centralized. | Covered by R08/R10; older section copies are F07. |
| Accordion (`accordion-new`) | NEEDS FIX | Shared item fragment and core runtime are reusable, keyboard-native, and expose content without JS. Fixed h3 skips a level in the FAQ composition. | F06; heading level should follow placement. |
| Divider / List | READY | Scoped component CSS; native hr/list markup. Heavy-content List renderer uses the existing class contract. | R10; do not count matching list markup as an independent implementation. |
| Table of Contents | NEEDS FIX | Good nav/list/fragment semantics and scoped component CSS; enhancement lives at `templates/content/content.js`. | F03; retain working no-JS links. |
| Text Input / Label / Checkbox / Radio / Select / Textarea | READY | Native controls, labels and dedicated CSS; existing contact and core behavior supplies validation/enhancement. | R09; no claim that every legacy disabled/read-only example is newly verified. |
| Input Affix / field composition | NEEDS FIX | Text affix is reused in form fields, but supporting layout and required-mark styles are template-owned. Other affix states are reference examples, not proven generic dropdown behavior. | F10. |
| File Upload | NEEDS FIX | Native file input and accessible labels exist. File selection/removal/validation used by contact is implemented in `templates/contact/contact.js`; layout repairs are in contact CSS. | F03/F10; document/extract the reusable behavior when packaging it independently. |
| Progress Indicator | NEEDS FIX | Central CSS and item fragments; current step semantics and mobile summary exist. Runtime update logic lives inside the form demo. | F03; do not confuse step presentation with a complete journey engine. |
| Page Feedback / Service Rating | READY | Shared composition and scoped, adapter-driven behavior; native fieldsets and status/error states. | R11. |
| Tab | NEEDS FIX | Shared presentation and semantic contract exist; service-specific JS implements ARIA, roving focus, RTL arrows and panels. No generic mounted tab controller is supplied by core. | F03/F08; existing service tabs are not broken. |
| Legacy Link / Accordion packages | DUPLICATE | `docs/decisions/001-canonical-components.md` explicitly selects `link` and `accordion-new`. Old packages share namespaces but are excluded from the site asset list. | F07; preserve source references and clarify legacy status, not automatic deletion. |

Other reference packages (Avatar, Chip, Tag, Slider, Content Switcher, Rating, Pagination, Quote, alerts, toast, floating button and code snippet) were not behaviorally qualified in this audit. Their existence does not mean MISSING, and historic `compliance.json` metadata is not proof of present failure or success. They should stay outside an unqualified “all components production-ready” claim until specifically assessed for a product use case. Tag/Rating consumption in services/feedback is distinct from certification of their full standalone variant surfaces.

## Sections Audit

| Section | Status | FACT — composition, inputs and dependency | Recommendation / finding |
|---|---|---|---|
| Page Intro | NEEDS FIX | Slots and variants work; styles live in government composition CSS; several internal pages bypass it. | R12, F01, F03. |
| Feedback | READY | Thin section wrapper injects rendered component and updated date; statistics are optional. | R11; retain local-preview distinction. |
| FAQ | NEEDS FIX | Questions are rendered from arbitrary validated records using the shared accordion item. FAQ CSS and core bootstrap live under the FAQ template. | F03/F06. |
| Contact CTA | NEEDS FIX | Configurable title, description, href and label; composes Card and Button class contracts. Depends on FAQ CSS, FAQ icon asset and government `.home-feature-icon`. | F03. This is real shared CSS reuse, not a duplicated Card implementation. |
| Heavy Content | NEEDS FIX | Structured sections/subsections and block types, shared TOC/Breadcrumb/List; own title block and placeholder-only media. | F01/F03/F11. |
| Hero | NEEDS FIX | Configurable title/description and slide data, but service destination, imagery and runtime belong to the government example. | F03/F09; generalize only demonstrated inputs. |
| About / statistics | NEEDS FIX | Data-driven text and statistic values; renderer zips entries with four fixed icons, limiting output to four. | F09; make this limit explicit or remove it deliberately. |
| Home services / catalogue | READY | Both consume the canonical service renderer; carousel vs filtered grid is a meaningful presentation difference. | Keep shared cards; F03 concerns packaging of the section runtime/CSS. |
| News | NEEDS FIX | Shared Card/Button/Grid, but all cards hardcode one image and `news.html#id`; builder takes only the first three. | F09; explicit limit/image/destination inputs. |
| Partners | NEEDS FIX | Data-driven names and reused Card; fixed section IDs, government carousel CSS/JS and placeholder glyphs. | F03/F09. |
| Simple content | READY | `sections/content/item.html` is a reusable semantic article using `.ds-prose`/`.ds-reading`; title/details/id are escaped by the renderer. | Preserve simple composition; rich content need not replace it. |
| Services / service-details (older alternatives) | DUPLICATE | Builder still supports these branches, but current configured pages use the newer catalogue/detail path. | F07; clarify supported versus historical pathways. |
| Service overview | NEEDS FIX | Reuses Card, Button, Tab, Service Card and feedback but owns intro/breadcrumb, support, related and FAQ assembly. | F01/F02/F03. Native details FAQ is a valid alternative, not a proven accessibility defect. |
| Contact | NEEDS FIX | Data-rendered fields/channels and explicit submission adapter; embeds its own intro/breadcrumb and file behavior. | F01/F02/F10. |
| Form | NEEDS FIX | Uses featured Page Intro, progress fragments and text-control classes. Variants configure a field-state demonstration, not per-step submission content. | F03/F10; label maturity accurately. |
| Error State | READY | Validated code/copy/action data; native heading and anchor, decorative assets hidden from accessibility APIs. | May remain under error template ownership until a second consumer requires packaging. No mandatory Page Intro for this system state. |

## Page Intro Audit

**FACT — expected template slots:** all are present: `breadcrumb_markup`, `eyebrow_markup`, `title`, `description_markup`, `extra_content_markup`. The renderer escapes title/text and inserts only designated HTML slots as markup. Extra rich markup is a trusted build-time input, not an untrusted HTML sanitizer.

| Variant | Verified implementation |
|---|---|
| default | Empty modifier suffix; outputs `.page-intro` alone. Selected when neither explicit variant nor description is supplied. |
| compact | `page-intro--compact`; smaller vertical padding and responsive heading rules; used by FAQ. |
| description | Selected automatically for description text; emits its modifier and description slot. No separate modifier CSS is necessary because the base/description element rules supply its appearance. |
| featured | Larger content gap; extra block can be provided. Form explicitly selects it and supplies the required-field note. |
| decorative | Pseudo-element radial decoration in composition CSS; no extra asset required. |

**FACT — Breadcrumb reuse:** `scripts/page_intro_markup.py:render_page_intro` calls `components/breadcrumb/two-level.html`. It does not reconstruct breadcrumb HTML. Root label/destination are currently fixed to Arabic Home / `index.html`; arbitrary depth and localized root labels are not renderer inputs (F02/F09).

**FACT — backward compatibility:** `SiteTests.test_page_intro_variants_optional_content_and_existing_faq` passed on this audit. It verifies all five variants, optional descriptions/extras, escaping, rejection of an unknown variant, and the existing FAQ rendering with compact styling classes and no unresolved breadcrumb slot. The build uses a temporary output directory. This proves those markup paths, not pixel equivalence of all consumers.

Current direct consumers are services, news, about and FAQ; form invokes the same renderer internally. Contact, heavy content and service details retain their own heading assembly (F01). Home hero and error state are intentional exceptions. Form's grid placement and nested-container override in `templates/form/form.css:10–11` are reasonable contextual layout rules; they do not prove a separate intro implementation.

## Templates Inventory

`site/government.json` configures nine pages. `scripts/build_site.py` generates six service-detail pages, for **15 page outputs and 10 main template/use-case families**. All use `templates/government/page.html`; a dedicated folder per output is not required. `templates/error/template.html` is an additional fragment, not the main shell selected by the builder. Component showcases, fixtures and generated `dist/` assets are not extra commercial templates.

All main outputs share Digital Stamp, Navigation Header, Footer, base styles and tokens. Feedback is present on all except error. “Suitable” below means inclusion as a documented library example, not a working backend product.

| Main template/output | Purpose and maturity | Reuse | Local duplication / CSS / missing abstraction | Classification; v1.0 suitability |
|---|---|---|---|---|
| Home — `index.html` | Complete illustrative landing composition; prior home report says implemented with documented differences, production_ready false. | Hero, About, Service Card carousel, News, Partners, Feedback. | Government composition CSS owns reusable section headings, carousel, hero and news image; fixed routes/limits/assets (F03/F09). | NEEDS FIX; include after packaging/documentation stabilization. |
| Services — `services.html` | Functional client-side searchable/filterable catalogue; prior service results recorded. | Page Intro, Service Card, Tab-styled filter buttons, native search, Feedback. | Catalogue CSS/JS under service template; generic search remains separate future scope (F03/F13). Filter buttons correctly use pressed states rather than pretending to be tabs. | NEEDS FIX; suitable after shared-dependency contract is explicit. |
| Service detail — `service-new-request.html`, `service-follow-up.html`, `service-support.html`, `service-service-4.html`, `service-service-5.html`, `service-service-6.html` | One shared data-driven detail template; launch is preview unless configured. | Service overview, Card, tags, tab styles, related Service Cards, Service Rating. | Local title and three-level breadcrumb; service-owned tab behavior/support/related sections (F01–F03). | NEEDS FIX; include as a preview-capable service-detail example after P1 work. |
| News — `news.html` | Simple text article listing, not a dedicated media/news-detail product. | Page Intro, simple content items, Feedback. | No duplicated article CSS; home news card input limits are F09, not a reason to invent a new listing. | READY for documented simple content scope. |
| About — `about.html` | Informational content including shell-linked anchors. | Page Intro, simple content, Feedback. | Uses shared typography/layout without a parallel content stylesheet. | READY within its current content scope. |
| Contact — `contact.html` | Validating local form with explicit async adapter and contact channels; prior contact results recorded. | Fields, Select, Textarea, File Upload, Card, Feedback. | Local intro/breadcrumb and field/upload styling; reusable data is mixed with fixed heading labels (F01/F02/F10). | NEEDS FIX; suitable after P1 stabilization; backend remains integration work. |
| FAQ — `faq.html` | Configured questions, progressive accordion, contact CTA; prior FAQ results recorded. | Compact Page Intro, Accordion, Card/Button CTA, Feedback. | Shared section CSS under FAQ; h1-to-h3 jump (F03/F06). | NEEDS FIX; include after ownership work, with heading improvement recommended. |
| Heavy content — `content.html` | Structured rich content and sticky/mobile TOC; prior content results recorded. | Breadcrumb, TOC, List, Divider styles, Feedback. | Independent header; rich block media only renders a placeholder (F01/F11); section CSS in content template. | NEEDS FIX; text/list scope usable, real media support not complete. |
| Form — `form.html` | Field-state and step-indicator demonstration; next/previous updates progress while the same fields remain. | Featured Page Intro, Progress Indicator, Text Input, Input Affix, Button, Feedback. | Required marker comes from contact CSS; progress runtime is demo-owned (F03/F10). No actual multi-step form schema. | EXPERIMENTAL; include only as an explicitly labelled example, not a complete transaction flow. |
| Error — `error.html` | Data-driven system outcome page with action; normal shared shell, no Feedback. | Error State, Button anchor and global partials. | Error-specific illustration/style ownership is justified; no need to force Page Intro. | READY for current 404/system-message scope; no fresh browser validation here. |

## Reuse & Duplication Findings

The following entries and those in subsequent sections constitute the 13 unique issues. Repeated references elsewhere do not increase counts.

| Item | Status | Severity | Evidence — FACT | Recommendation |
|---|---|---|---|---|
| F01 — Parallel internal-page introductions | DUPLICATE | P1 | `sections/contact/template.html` embeds `.contact-page__intro` and h1; `sections/heavy-content/template.html` embeds `.heavy-content__header`; `sections/service-overview/template.html` embeds `.service-page__title`. Their typography/layout rules live in the corresponding template CSS. None calls Page Intro. Registry claims all internal headings use it. | Migrate compatible title areas through existing slots/variants, preserving reference-specific layouts. Do not alter home/error exceptions or flatten materially different layouts blindly. |
| F02 — Breadcrumb assembly paths | DUPLICATE | P1 | Canonical two-level fragment exists; `scripts/service_markup.py:overview` constructs a three-level nav string with a template asset. `sections/contact/template.html:2` builds another nav with different li/link classes, and contact CSS redefines list styling. | Extend Breadcrumb to accept an item list/variable depth, then use it from Page Intro and the exceptional compositions. Retain valid semantics and direction-specific separators. |
| F07 — Historical component/section alternatives remain discoverable | DUPLICATE | P2 | Legacy `accordion`/`dga-links` are deliberately retained by decision 001 and not loaded by the site. `sections/home-services/card.html` is not used by the current `home-services` branch, which calls canonical `service_card()`. Older services/card and service-details branches remain available but unused by configured pages. | Mark old section paths and canonical replacements clearly, as already done for Link/Accordion. Do not count reference-only `card-bk` JSON as runtime duplication or delete reference assets automatically. |

**Not duplication:** Card class-contract markup in distinct composites; the same header/footer emitted into each generated static page; native details for service FAQ versus enhanced accordion where distinct behavior is intentional; simple article layout versus rich content with a TOC. No exhaustive text duplicate scan was performed.

## CSS Architecture Findings

| Item | Status | Severity | Evidence — FACT | Recommendation |
|---|---|---|---|---|
| F03 — Reusable sections/runtime rely on template asset ownership | NEEDS FIX | P1 | Page Intro, section-heading, carousel, news-image and shell search CSS live in `templates/government/composition.css`; Contact CTA/FAQ CSS lives in `templates/faq/faq.css`. CTA also uses a FAQ icon and government home-feature-icon. Heavy-content CSS/TOC JS lives in `templates/content/`; tabs/catalogue JS in service; progress JS in form; upload JS in contact. `build_site.py:ASSETS` and the global shell load all template styles/runtimes, hiding these extraction dependencies. | Establish section/component-owned dependency bundles or explicit reusable ownership before claiming portable v1.0. Keep genuinely page-grid and illustration rules local; do not move every rule solely because of its folder. |
| F10 — Shared field presentation depends on Contact | NEEDS FIX | P1 | `scripts/form_markup.py:41` uses `.contact-required`; its style is defined only in `templates/contact/contact.css:15`. Identical text-input label overrides occur in contact CSS:14 and form CSS:19. Form also supplies affix sizing, and contact supplies reusable upload wrapping repairs. | Consolidate the demonstrated required marker/field presentation into an existing field component or safe shared variant; preserve spacing differences owned by each form layout. Verify contact and form together after a future fix. |

The current all-assets shell means F03/F10 are portability and maintenance defects, not evidence that styles are presently missing on built pages. Central Button/Card/Breadcrumb CSS is already reused; no new universal component is justified merely to eliminate short assembly fragments.

## RTL / Responsive Findings

**FACT:** layout and major templates generally use logical sizing/padding, flexible tracks and 767/768 breakpoints. Header uses a synchronized 960px CSS/JS breakpoint (`navigation-header.css` and `navigation-header.js`); component-specific navigation collapse is not inherently wrong because base grid uses 768px. Breadcrumb flips separators, contact handles its custom arrow, and service tabs reverse horizontal arrow-key navigation in RTL.

**FACT:** existing base, header, footer, service, contact, FAQ, content and form result files contain RTL/LTR viewport cases. These are prior evidence only. This audit does not claim a fresh mobile overflow, mixed-direction nesting, long-label or contrast pass.

**Recommendation:** when addressing F01/F02/F03/F10, run focused RTL/LTR desktop/mobile checks on changed consumers, especially the form nested container, service title/sidebar and contact breadcrumb. Do not introduce a separate RTL stylesheet. No additional verified directional defect is counted on the basis of physical properties alone.

## Accessibility Findings

| Item | Status | Severity | Evidence — FACT | Recommendation |
|---|---|---|---|---|
| F05 — Disabled Link reference contradicts execution contract | NEEDS FIX | P1 | `components/link/template.html:34,54,75` retains `href="/destination"` with `aria-disabled="true"` and tabindex -1. `docs/core-qualification.md` requires href removal and explicitly notes the guard cannot prevent context-menu navigation. | Align copyable reference examples with the established native/ARIA contract. This is a reference-package defect; no claim is made that current government navigation has disabled links. |
| F06 — FAQ heading level is fixed too deep | NEEDS FIX | P2 | Page Intro supplies h1; `sections/faq/template.html` has an aria-label but no h2; `components/accordion-new/item.html` fixes each question at h3. A labelled section does not create an h2. | Choose the question heading level by placement or add a meaningful section heading. The jump is an outline quality issue, not proof the accordion fails keyboard interaction. |
| F08 — General core enhancement is only mounted inside FAQ | NEEDS FIX | P2 | `templates/faq/faq.js` calls `initCore` only for `[data-faq]`; no global core mounting is included by the shared shell. Core contains disabled Button/Link and special Checkbox behavior in addition to Accordion. | Document the shell's mounting contract and supply deliberate initialization when those enhanced variants are introduced elsewhere. Existing native controls/current FAQ behavior are not reported as broken. Avoid overlapping core roots. |

Native controls, skip navigation, hidden fallbacks, label/error associations, status regions and Escape/focus restoration are positive evidence (R04–R11). Formal accessibility compliance remains unverified. Prior records explicitly say formal compliance is pending; historical `not_run` rules must not be presented as newly passed or automatically failed.

## Foundation Gaps

| Item | Status | Severity | Evidence — FACT | Recommendation |
|---|---|---|---|---|
| F04 — Inventory and contracts lag implementation | NEEDS FIX | P1 | Registry says all internal headings use Page Intro despite F01. `docs/foundation.md` says no local fonts, while `assets/fonts/fonts.css` and build assets supply them. Card contract says component tokens are missing, but `token.css` defines them; its mandatory Avatar wording conflicts with current static consumers. `docs/inventory.json` retains planned records for capabilities now represented by live sections. | Reconcile current contracts, registry consumers, inventory and release qualification scope. Preserve dated test history; do not mark legacy rules passed without evidence. |
| F09 — Reusable composition has implicit content/route constraints | NEEDS FIX | P2 | `build_site.py:validate` requires index/services; footer legal links are fixed to about anchors; Page Intro root label is Arabic; contact heading is fixed; hero/about/news routes and news image are hardcoded. Statistics uses zip with four icons; news truncates to three. | Make recurring routes, labels, image metadata and display limits explicit inputs, or document bounded government-example contracts. RTL support alone is not multilingual content configuration. |
| F11 — Heavy-content media has no asset input/rendering path | NEEDS FIX | P2 | `scripts/content_markup.py:_render_block` always renders `.heavy-content__media-placeholder` with role img for a media block. Validator accepts alt/caption but has no media source contract. | Add a validated asset-backed media variant when required; retain an explicit placeholder for demonstrations. Current placeholder presentation is intentional, but not complete rich-media support. |
| F12 — Reusable table pattern | MISSING | P2 | No table implementation is present in the inspected `components/` inventory or section/build paths; heavy content's `BLOCK_TYPES` excludes tables. | Add a semantic, responsive table contract when real tabular content is required. Do not block text-only v1.0 examples or create a dashboard preemptively. |
| F13 — General site search/results capability | MISSING | P2 | Existing header search renders only service links and uses government home JS; catalogue filters only service records. Configured pages and build branches contain no general results section/template. | Define generic search/result inputs before a product promises whole-site search. Reuse existing search field, links and list patterns; backend indexing is a later integration concern. |

There is already a form primitive foundation; a production multi-step transaction engine is not implied by the current form demo. Similarly, contact/feedback adapters and configurable service launch URLs are deliberate integration seams, not missing backends to build during stabilization.

Events/documents/quick links and other planned generic sections in `docs/architecture.md` need an explicit release-scope decision; a planned inventory row alone is not evidence of a defect. No College, Minister, Academic Program or other sector-specific template is listed as a foundation gap.

## Recommended Fixes Before v1.0

Six P1 findings should be resolved before labelling the shared foundation stabilized:

1. **F01:** complete compatible Page Intro adoption while preserving approved page composition.
2. **F02:** give the existing Breadcrumb a reusable variable-depth assembly path.
3. **F03:** make shared section/component asset ownership portable and explicit; preserve contextual template CSS.
4. **F10:** remove the form-to-contact required-marker dependency and duplicated shared field presentation.
5. **F05:** align disabled Link examples with the already-approved execution contract.
6. **F04:** reconcile the registry/contracts/inventory with actual consumers, dependencies and validation scope after the above decisions.

These are recommendations only. No fix was implemented. Future validation should target changed components and known consumers once; shared shell changes justify a bounded wider check at that time, not a full suite during this audit.

## Deferred Improvements

Seven P2 issues can follow stabilization: FAQ heading flexibility (F06), clear legacy section status (F07), deliberate core mounting outside FAQ (F08), configurable reusable content/route inputs (F09), real heavy-content media (F11), a semantic table pattern when needed (F12), and general search/results when required (F13).

Dynamic variants not used by current templates should be qualified individually before adoption; no broad rewrite or framework migration is recommended. Current experimental form behavior should remain clearly described rather than silently promoted to a transaction product.

## Foundation v1.0 Readiness

**Decision: not yet ready for an unconditional Foundation v1.0 release; ready for bounded prototyping and continued reuse.** There are no established P0 blockers. Central tokens/base, global partials, native controls, static content primitives, service cards and feedback provide a substantial reusable base. Six P1 items separate that base from a dependable portable release.

Ministry and university informational products can already compose the shared shell and content sections. A services portal can reuse catalogue, details and field primitives, with explicit product integration for submission and search. None should inherit a promise that every reference component is behaviorally certified or that the form demo is a complete transaction flow.

Validation performed in this audit: static inspection plus **one passing existing Page Intro test** (`tests/test_site_build.py:75`). It exercised a temporary build, all requested variants and existing FAQ markup compatibility. Historical result files were consulted as historical evidence. No full static audit, browser test, E2E run, visual regression, external reference comparison or fresh formal accessibility verification was performed.
