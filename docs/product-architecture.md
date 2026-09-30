# Product Architecture

Status: approved architecture with the Ministry product boundary and M01 registry/data seam implemented. M02–M03 register shared Heavy Content pages, and M04 adds the first Ministry-owned page template. No Foundation source moved and no stabilization finding was reopened.

## 1. Executive Decision

Keep this repository as one source-of-truth monorepo. Preserve the stabilized Foundation in its current top-level paths and add an explicit `products/<product-id>/` layer for each commercial website product. A product owns sector-specific composition, configuration, demo content and assets; it references Foundation source rather than containing a copy.

The current top-level `templates/` layer remains the home of reusable page capabilities that sit above a section but below a sector product. The current government shell is shared infrastructure during migration. A Ministry-only page is placed under `products/ministry/`; it is promoted only after another product proves that the same semantic contract is useful.

The first additive migration is implemented: the Ministry descriptor selects the existing rendering pipeline through a compatibility adapter. Current renderers, Foundation paths, `site/government.json` and the legacy CLI remain available.

## 2. Current Architecture Summary

The repository already follows most of the intended dependency direction:

```text
token.css + assets/fonts + styles/base
                    ↓
              components
                    ↓
        partials + reusable sections
                    ↓
       reusable page templates/renderers
                    ↓
 templates/government/page.html shell
                    ↓
           site/government.json
                    ↓
         scripts/build_site.py
                    ↓
           dist/government/
```

`site/government.json` currently combines product identity, language and direction, header/footer configuration, page registration, section order, service collections and all demo content. `scripts/build_site.py` validates that single shape, dispatches a fixed list of section IDs, creates configured pages plus generated service-detail pages, selects CSS and scripts, and copies assets. Its CLI accepts `--config` and `--output`, with one government default.

All generated pages use `templates/government/page.html`. That shell composes the skip link, Digital Stamp, Navigation Header, main landmark and Footer. Shared field, Breadcrumb, Page Intro and runtime ownership follow the stabilized contracts. The output is a self-contained static site, but product identity is implicit in the config and output paths rather than represented as an architectural object.

The main boundary issues for product work are:

- one data file mixes reusable configuration, product structure and example content;
- the builder knows section names, global asset lists and government defaults directly;
- top-level reusable templates and the government shell are not distinguished from a commercial product by an explicit manifest;
- `templates/government/home.js` is currently loaded by the shell on every page even though its behavior is composition-specific;
- generated service pages are registered indirectly from the services collection.

These are product orchestration concerns. They do not invalidate or require changes to Foundation v1.0.

## 3. Product Boundary Model

| Boundary | Owns | Must not own |
|---|---|---|
| A. Foundation | Tokens, fonts, Base CSS, layout primitives, shared components, shared sections, shared partials, common shell semantics and component runtimes | Sector page lists, ministry content, customer branding data, sector-only templates |
| B. Shared reusable template capability | Page-level composition used by more than one product: Content Detail, Service Detail, Form, Contact, FAQ and Error/Outcome patterns; integration code that coordinates their shared components | Product navigation, sector-specific fields, client content, a Foundation primitive duplicated for convenience |
| C. Product | A complete commercial sector website definition, its supported page/content types, default composition policy, product assets and build entry point | Copies of Foundation source or unproven abstractions for other sectors |
| D. Product-specific page/template | Semantic structures unique to the product, such as Minister Profile, Ministry Organization Structure, Academic Program or Municipality Project | Generic H1, Breadcrumb, Header, cards or field primitives already supplied by Foundation |
| E. Product configuration/content | Product ID, shell choice, locales, route registration, navigation/footer data, page composition and product copy | Executable renderer paths supplied by arbitrary data or generated build artifacts |
| F. Demo/example data | Fictitious content used to preview and sell the product; clearly separated from structural configuration | Official claims, customer production content or canonical component contracts |
| G. Generated output | Resolved static HTML and only the assets required to deploy one product | Hand-edited source, reusable ownership or input for another product build |

Dependencies flow from Product to shared templates to Foundation. Foundation never imports a product. One product never imports another product's private templates or assets.

## 4. Recommended Repository Structure

The implemented boundary is additive. Existing top-level paths remain canonical, and no directories for future products were created.

```text
.
├── token.css                         # Foundation
├── assets/
│   └── fonts/                        # Foundation assets
├── styles/
│   ├── base/                         # Foundation
│   └── composites/                   # Existing shared capability
├── components/                       # Foundation components
├── sections/                         # Foundation/shared sections
├── partials/                         # Shared shell partials
├── templates/                        # Shared page capabilities
│   ├── government/                   # Existing shared government shell
│   ├── contact/
│   ├── content/
│   ├── error/
│   ├── faq/
│   ├── form/
│   └── service/
├── scripts/                          # Shared render/build implementation
├── products/
│   └── ministry/
│       ├── README.md                  # Boundary and build command
│       ├── product.json               # Product manifest / entry point
│       ├── navigation.json            # Product-owned navigation
│       ├── footer.json                # Product-owned footer
│       ├── pages/
│       │   ├── index.json             # Authoritative page registry
│       │   ├── about.json
│       │   ├── strategy.json
│       │   └── minister.json
│       ├── content/
│       │   └── demo/                  # Fictitious product records
│       ├── templates/
│       │   └── minister-profile/      # First Ministry-only renderer/template
│       └── assets/
│           └── minister-profile/      # Fictitious portrait placeholder/source note
├── site/
│   └── government.json               # Transitional current config
└── dist/
    └── products/
        └── ministry/                  # Generated; never edited as source
```

Top-level `templates/` means cross-product page capability, while `products/<id>/templates/` means a product-specific semantic page. The name `templates/government/` is historically ambiguous; keep it during migration and document it as the shared shell. A future rename is optional and should happen only as a separate migration after multiple products use the shell.

## 5. Foundation vs Product Ownership

Foundation owns a capability when its semantics and accessibility contract make sense without a sector. A product owns a capability when its data model, language or information architecture is specific to that sector. Visual similarity alone does not establish shared ownership.

| Capability | Initial owner | Reason |
|---|---|---|
| Header / Footer | Foundation components and shared partials | Their structure and behavior are common. Ministry supplies navigation, labels, links and branding configuration. |
| Breadcrumb / Page Intro | Foundation | They solve common internal-page navigation and heading semantics and already have stabilized shared renderers. |
| Service Card | Foundation | It is an existing reusable component with a sector-neutral service contract. |
| News Card | Private child of the existing News section initially | The current implementation is not yet a standalone qualified component. Extract it only when a second context needs the same contract. |
| Contact, FAQ, Form, Content Detail, Service Detail | Shared reusable template capability | They coordinate Foundation assets at page level and are not Ministry concepts. Product configuration supplies their routes and content. |
| Minister Profile / Ministry Organization Structure | Ministry product | The semantics and data model are ministry-specific. |
| Academic Program / College Page | University product | They express educational entities and relationships. |
| Municipality Project | Municipality product | Its status, geography and municipal data belong to that product until reuse is demonstrated. |

Ministry reuses Header and Footer through the existing shell and partial renderers. It reuses components and sections by stable IDs in registered renderers; product templates compose their canonical source files. It does not copy HTML, CSS or JavaScript into `products/ministry/` merely to change text or section order.

Foundation ownership also does not imply that every inventory item is production-qualified. The status and evidence rules in `docs/foundation.md` and `docs/inventory.json` continue to apply.

## 6. Product Configuration Model

Use small JSON files with distinct responsibilities. Do not introduce a generic CMS schema.

`product.json` is the implemented build entry point. Its v1 boundary schema contains `schema_version`, immutable product `id`, product `name`, the transitional `source_config`, and relative paths for `navigation`, `footer`, `pages`, `templates`, `demo_content` and `assets`. All owned paths are validated to remain inside the product directory; `source_config` must remain inside the repository.

`navigation.json` and `footer.json` own the product information architecture and labels loaded by the product command. `pages/index.json` is the authoritative v1 page registry; M02 and M03 register `about.json` and `strategy.json` through the shared Heavy Content renderer, while M04 registers `minister.json` through the product-scoped `minister-profile` renderer. Its `pages` list contains validated JSON references within `pages/`. Each referenced definition contains only a lowercase `id`, a flat `.html` `route`, an allow-listed `renderer` ID and a `content` JSON reference relative to `content/demo/`. The loader rejects duplicate routes and IDs, unknown renderer IDs, missing page/content files and references that escape either owned root. Content is data only and cannot define route, renderer, template or section selection. A separate content index is not required by this direct-reference model.

Page composition configuration owns ordered section IDs and explicit supported options. Demo copy and collection records live under `content/demo/`. This permits a future customer content input without changing product structure, while keeping the current repository static and template-oriented.

Feature flags should not be added pre-emptively. Presence in page registration, a documented renderer option or an existing component variant is enough for v1. Add a product feature flag only when it changes behavior across several routes and cannot be represented by page registration.

The Ministry manifest currently points through `source_config` to `site/government.json`. The adapter overrides navigation and footer with product-owned files, then replaces or appends routes registered in the product page registry. Unregistered pages and other unmigrated concerns remain transitional. The compatibility field is removed only after every concern it still supplies has migrated.

## 7. Build Strategy

The current builder received a narrow orchestration extension rather than a rewrite. The implemented command is:

```sh
python3 scripts/build_site.py --product ministry
```

1. `--product ministry` resolves `products/ministry/product.json`; invalid or unknown product IDs fail before a build begins.
2. `--config` and `--output` remain available. Running without arguments still builds `site/government.json` to `dist/government/`.
3. The loader validates the manifest and owned paths, loads product navigation/footer and the product page registry, resolves page content inside `content/demo/`, dispatches its allow-listed renderer ID and normalizes the result into the current data contract.
4. The existing `render()` function and specialized markup modules remain unchanged in role.
5. The default selected-product output is `dist/products/ministry/`; `--output` remains available for focused tests and integrations.
6. Product assets are copied to the namespaced output path `assets/products/ministry/`. A fixed product renderer registration may load a module and stylesheet contained by the product template root; M04 proves this path with Minister Profile while page JSON remains unable to select executable files.
7. Existing implicit service-detail generation is retained by the compatibility build.

The long `if/elif` section dispatch and hardcoded asset lists can be split into registries later when a second product creates real pressure. They are not a prerequisite for the Ministry boundary and should not be refactored in the first step.

## 8. Product Asset Strategy

Source ownership remains singular:

- Foundation CSS, JavaScript, fonts and component assets stay in their canonical top-level paths.
- Shared template capability keeps template-owned integration styles and scripts in top-level `templates/`.
- Ministry-only media, composition CSS and behavior live under `products/ministry/` and use product-scoped class names where appropriate.
- The builder resolves a page's dependency set and copies each destination once. A release artifact may contain copies of required Foundation files because it must deploy independently; this is packaging, not duplicate source ownership.

Preserve deterministic loading order: tokens and fonts, Base, Foundation components, shared sections/templates, then product composition. Load runtime dependencies before the integration that consumes them. Extend the current `STYLE_SECTIONS`, `page_styles()` and `page_scripts()` mechanism initially; do not introduce a dependency-graph system before multiple products justify it.

Product assets should be emitted under a namespaced path such as `assets/products/ministry/`. Shared output paths should continue to mirror their canonical source paths so existing relative references work. The generated package must include licenses and source notices for copied assets.

The current unconditional shell load of `templates/government/home.js` should become a registered home/product script when product-aware asset selection is implemented. This is a future product-build correction; it is not a Foundation ownership change in this analysis.

## 9. Template Ownership Rules

Use this decision sequence for every new page type:

1. Compose the page from existing Foundation components, sections and a shared template capability.
2. If the remaining structure is meaningful only in one sector, place its template and renderer under that product.
3. Keep page content and route data out of HTML templates.
4. Add a shared variant only when the difference is presentational and the existing semantic contract remains intact.
5. Do not move a product template into Foundation on the expectation that another product may need it.

A product template may control its page grid, sidebar relationships, section order and sector data mapping. Foundation continues to own intrinsic component presentation, accessibility and behavior. For example, Minister Profile may own biography metadata and ministry relationships while reusing Page Intro, Avatar, cards, links and shared content sections.

Top-level shared templates own reusable page orchestration, not a customer's complete page catalogue. Product routes select them; products do not fork them.

## 10. Cross-Product Promotion Rules

Promotion is evidence-driven:

```text
product-specific capability
          ↓
second independent product needs the same semantic structure
          ↓
compare data, states, accessibility, responsive behavior and integration
          ↓
extract the smallest stable common contract
          ↓
place it in shared templates, sections or Foundation at the correct layer
          ↓
migrate both consumers, validate them, remove duplicate source, update registry
```

A second consumer triggers evaluation; it does not force promotion. Keep the capability local if shared use would require sector switches, many empty slots or different semantics. Record the decision in `docs/component-registry.md` or an architecture decision when promotion affects a public contract.

## 11. Variant Strategy

V1 uses one named default composition per product page type. Existing Foundation variants, such as Page Intro variants, remain available through their current contracts.

Future `A`/`B` page choices should be explicit registered variants of one semantic renderer when only layout or presentation changes. If structure, behavior or accessibility differs materially, register a separate template capability. Product page configuration may select a supported variant ID; it may not select arbitrary HTML or CSS paths.

Do not add a global variant engine, feature-flag matrix or parallel CSS bundle now. Establish the first Ministry page catalogue, then add only the variant mechanism required by a verified second composition.

## 12. Commercial Packaging Direction

The monorepo remains the authoring source. A product build produces a self-contained static release under `dist/products/<product-id>/` containing:

- generated HTML for registered routes;
- the resolved Foundation/shared/product asset subset;
- local fonts and required licenses/source notices;
- a small release manifest recording product ID/version, Foundation version, locale/content profile and build timestamp or reproducible build identifier.

The package must not contain other products' private source or unused demo content. Packaging can later wrap this directory as a ZIP or deployment artifact without changing source ownership. Customer production content should be supplied as a separate validated input or downstream integration; the repository's demo profile remains safe preview data.

## 13. Migration Plan From Current Structure

1. **Introduce the boundary — complete.** `products/ministry/product.json`, product-owned navigation/footer, empty ownership directories and `--product ministry` are present. The current `--config`, `--output`, renderers and legacy default remain working.
2. **Prove equivalent compatibility output — complete for the boundary.** Focused tests compare the product and legacy page lists, resolve shared assets and verify the product default output path. Visual certification is outside this architecture step.
3. **Separate configuration gradually.** Move one concern at a time from the monolithic current config into navigation, footer, page registry and demo content files. The normalizer supports old and new input during the transition; each concern has one authoritative source for the same configuration.
4. **Add Ministry-only page types incrementally.** New sector pages live under `products/ministry/` and compose Foundation/shared capabilities. Existing generic page templates remain top-level.
5. **Make packaging explicit.** Generate the Ministry release directory and manifest from its product descriptor. Verify that it has no dependency on another product directory.
6. **Add the second product.** Start University only after the Ministry boundary and package are stable. Use actual overlap to evaluate promotions; do not pre-create its directories or abstractions.

No step requires moving the stabilized Foundation. Any later rename of the government shell or shared templates should be isolated, compatibility-tested and recorded separately.

## 14. Risks / Decisions Required

| Risk or decision | Direction |
|---|---|
| Meaning of “government” | Treat the existing `templates/government/page.html` as a shared shell during migration, not as the Ministry product. Revisit its name only after another product consumes it. |
| Product ID naming | Use stable lowercase slugs such as `ministry`, `university`, `government-services` and `municipality`; IDs become build and output identifiers. |
| Mixed current config | Use a temporary normalizer and remove the compatibility pointer once split files are authoritative. Do not maintain two editable copies. |
| Hardcoded builder dispatch/assets | Extend current registries first. Split them only when multiple products create real pressure. |
| Product-specific search in shared header | Keep the current behavior for compatibility. General site search remains deferred F13 and should become shared capability with a product-provided index/content adapter when scheduled. |
| Unconditional home runtime | Select it by registered page/product dependency in a later step; do not move its behavior into Foundation. |
| Route and content limits | Product manifests make ownership explicit, but configurable route rules remain deferred F09 until scheduled. Preserve current validation meanwhile. |
| Deferred F06/F07/F08/F11/F12 | Keep their documented status. Their likely owners are Foundation/shared capability, except product templates may consume them after they are addressed. This architecture does not mark them resolved. |
| Client customization | Keep sector product defaults and demo data in this repository. Define customer overlays only after a real need; avoid a speculative tenant/CMS layer. |
| Promotion pressure | Require two independent semantic consumers and migration evidence. Similar screenshots are insufficient. |

Resolved F01, F02, F03, F04, F05 and F10 remain closed. This document changes no implementation or qualification claim.

## 15. Recommended Next Step

Run a separate **Ministry Product Blueprint** analysis. Define the Ministry page/content-type inventory and map each type to an existing Foundation section, shared template capability or Ministry-only need. Keep that task separate from this boundary implementation; do not add Ministry templates or content before the blueprint is approved.
