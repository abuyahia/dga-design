# Ministry Required V1 — Existing vs New Mapping

Status: approved implementation mapping for the 16 REQUIRED V1 types. This document changes no Foundation source, page configuration, templates, Search implementation or demo content.

## 1. Executive Mapping

The current repository can satisfy six required types through configuration alone. Four types have a strong existing page capability but need a bounded Ministry composition or data contract. Six types have no suitable current template or behavior and require new work.

| Classification | Count | Meaning in this mapping |
|---|---:|---|
| REUSE | 6 | Current page capability satisfies the approved contract; Ministry data, registration and routes are sufficient. |
| ADAPT | 4 | Existing capability supplies most structure, but a bounded product composition or semantic data wrapper is required. |
| NEW | 6 | The required semantic listing, detail, hierarchy, profile or search contract does not currently exist. |

Only **Search Results** requires a new shared capability. Its Ministry index remains product-owned and any production search engine remains integration-owned. All other ADAPT/NEW work stays under `products/ministry/` for V1.

## 2. Mapping Summary

### Classification totals

| REUSE | ADAPT | NEW | Total |
|---:|---:|---:|---:|
| 6 | 4 | 6 | 16 |

### Complexity totals

| LOW | MEDIUM | HIGH | Total |
|---:|---:|---:|---:|
| 6 | 7 | 3 | 16 |

Complexity describes the template/data/build work for the page type. It does not include production backend integrations, content authoring or formal product certification.

## 3. Required V1 Mapping Table

| # | Required type | Classification | Existing source(s) | Foundation assets reused | Missing capability | Product-owned work required | Shared change? | Complexity |
|---:|---|---|---|---|---|---|---|---|
| 1 | Home | ADAPT | `templates/government/page.html`, `templates/government/composition.css`, `templates/government/home.js`, `sections/hero`, `sections/home-services`, `sections/news`, `sections/partners` | Shared shell, Header, Footer, Hero candidate, Service Card, Card, Button, Link, Feedback | Approved Ministry order, initiative/resource/contact composition, product data mapping and page-specific asset selection | Ministry Home composition and renderer registration | No | MEDIUM |
| 2 | About Ministry | REUSE | `sections/page-intro`, `sections/heavy-content`, `templates/content`, `scripts/content_markup.py` | Breadcrumb, Page Intro, Heavy Content, TOC, Divider, List, Link, Feedback | No structural gap | Page definition, Ministry content record and route | No | LOW |
| 3 | Minister Profile | NEW | No current profile template; reusable pieces in `sections/page-intro`, `components/avatar`, `sections/heavy-content` | Breadcrumb, Page Intro, Avatar candidate, Card, Link, content primitives, Feedback | Minister semantics, portrait/biography contract and profile composition | Ministry Minister Profile template, renderer and record schema | No | MEDIUM |
| 4 | Organizational Structure | NEW | No hierarchy page; only general Card/List/Link/Button primitives | Breadcrumb, Page Intro, Card, List, Link, Button, Feedback | Accessible hierarchical model and textual rendering | Ministry organization template, hierarchy validator and record schema | No | HIGH |
| 5 | Strategy, Vision and Objectives | REUSE | `sections/page-intro`, `sections/heavy-content`, `templates/content`, `scripts/content_markup.py` | Breadcrumb, Page Intro, Heavy Content, TOC, List, Link, Feedback | No structural gap for prose, objectives and attachments as links | Page definition, structured Ministry copy mapped to Heavy Content and route | No | LOW |
| 6 | Contact | REUSE | `sections/contact`, `templates/contact`, `scripts/contact_markup.py` | Page Intro, Breadcrumb, Card, Label, Text Input, Select, Textarea, File Upload, Button, Feedback | No page-template gap; production submission is an external adapter | Product channels, form labels/policy, route and optional submit adapter configuration | No | LOW |
| 7 | FAQ | REUSE | `sections/faq`, `templates/faq`, canonical Accordion and current builder branch | Page Intro, Breadcrumb, Accordion, Contact CTA, Card, Feedback | No structural gap for the approved simple FAQ | Question data, Contact CTA data and route | No | LOW |
| 8 | Search Results | NEW | Header currently contains service-only search; `search` remains planned in inventory and F13 is deferred | Page Intro, Breadcrumb, Label, Text Input, Select, Button, Link, Card/List, Tag, Pagination candidate, Feedback | Generic whole-site results/empty-state contract and content index | Ministry content-index adapter, indexed fields/type labels and route registration | Yes — shared Search/Results capability | HIGH |
| 9 | News Listing | NEW | `sections/news` is a three-card Home grid; `sections/content` is not a chronological listing contract | Page Intro, Breadcrumb, Card, Tag, Link, Button, Feedback | Editorial collection schema, dates, detail routes, empty state and listing composition | Ministry Editorial listing renderer and News configuration | No | MEDIUM |
| 10 | News Detail | ADAPT | `sections/heavy-content`, `templates/content`, `scripts/content_markup.py` provide body, Page Intro and TOC | Breadcrumb, Page Intro, Heavy Content, List, Link, Tag, Feedback | Article metadata, semantic editorial header, canonical date/route and related-content slots | Bounded Ministry Editorial detail composition around Heavy Content and shared record schema | No | MEDIUM |
| 11 | Services Catalogue | REUSE | `sections/service-catalog`, `templates/service`, `scripts/service_markup.py` | Page Intro, Service Card, Text Input, Button, Tag, Link | No structural gap for required query/audience filtering; Ministry category mapping is data | Service/category records, page registration and approved destinations | No | LOW |
| 12 | Service Detail | REUSE | `sections/service-overview`, `templates/service`, `scripts/service_markup.py` | Breadcrumb, Page Intro, Tabs, Lists, Buttons, Links, Service Card, rating, Feedback | No structural gap for approved required/optional service fields | Ministry service records, routes and operational URL adapters | No | LOW |
| 13 | Initiatives Listing | NEW | No Portfolio listing; reusable Card/Tag/Link primitives only | Page Intro, Breadcrumb, Card, Tag, Link, Button, Feedback | Initiative collection/status schema, detail routes, empty state and listing composition | Ministry Portfolio listing renderer with Initiative configuration | No | MEDIUM |
| 14 | Initiative Detail | ADAPT | Heavy Content supplies body sections, lists, links, Page Intro and TOC | Breadcrumb, Page Intro, Heavy Content, Card, Tag, List, Link, Feedback | Status/owner/objectives metadata and optional metrics/related slots | Bounded Ministry Portfolio detail composition and Initiative record schema | No | MEDIUM |
| 15 | Resources Library | NEW | `documents` is planned; no current library. File Upload is unrelated to publishing downloads | Page Intro, Breadcrumb, Text Input, Select, Card/List, Tag, Link, Button, Pagination candidate, Feedback | Resource-kind schema, filters, file metadata, accessible download actions, empty state | Ministry Resource library renderer, validator and record collection | No | HIGH |
| 16 | Resource Detail / Download | ADAPT | Heavy Content supplies descriptive body and in-page navigation; Link/Button supply destinations | Breadcrumb, Page Intro, Heavy Content, List, Link, Button, Tag, Feedback | Resource metadata header, file/version/format contract and download action | Bounded Ministry Resource detail composition and shared Resource record schema | No | MEDIUM |

## 4. REUSE Items

### About Ministry and Strategy, Vision and Objectives

Both fit the existing Heavy Content contract: Page Intro, optional descriptive grouping, Table of Contents, sections/subsections, paragraphs, lists and safe links. They need separate product records and routes. No new Ministry template is justified. Strategy metrics or advanced media remain optional; their absence does not change the classification.

### Contact

The current Contact template already provides the approved page structure, contact-information sidebar, accessible field primitives, file attachment behavior and adapter boundary. Ministry channels, categories, privacy/help text and any submit handler are configuration/integration. Field structure does not need to change for V1.

### FAQ

The simple FAQ contract already accepts an unbounded configured question list, uses the canonical Accordion and composes Contact CTA and Feedback. Ministry questions and routes are sufficient. Deferred FAQ heading flexibility F06 is not required by the approved V1 contract.

### Services Catalogue and Service Detail

The current shared service family already has one service record source, a searchable/audience-filtered catalogue, generated details, required steps/requirements/documents, optional operational metadata, related services and integration-owned start/support destinations. Ministry category taxonomy must be mapped into the existing catalogue data without creating category pages.

## 5. ADAPT Items

### Home

The government example is not directly reusable as the Ministry Home. It hardcodes service-only search data, Hero destinations, three News cards, four statistic icons and global `home.js` loading. Its shell and several sections are useful, but the approved Ministry Home also requires curated Initiatives, Resources and Contact CTA with product-owned ordering and data selection. Build a Ministry composition that consumes the existing sections and registers only its required assets. Do not copy `templates/government/` into the product.

### News Detail

Heavy Content already solves long-form body structure, Page Intro, TOC and safe blocks. A bounded Editorial detail composition must add published/updated dates, editorial metadata, canonical route and optional related items around that body. It remains paired with one NEW Editorial listing and should share the same product record contract.

### Initiative Detail

Heavy Content also supplies the main narrative structure. The Ministry Portfolio wrapper adds status, owner, objectives and optional verified metrics/related records. This is product adaptation because the portfolio semantics are Ministry-owned even though its body is shared.

### Resource Detail / Download

Heavy Content and Link/Button cover explanation and safe destinations. The Resource detail wrapper must add resource kind, version, format, file size, publication/update dates and an accessible primary download/external action. File Upload must not be reused: it is an input control, not a published-file presentation.

## 6. NEW Items

### Minister Profile

No current template represents the Minister's official role, portrait, biography and optional message/appointment metadata. Create one Ministry-owned template composed from Page Intro and existing content primitives. A generic Profile promotion is premature.

### Organizational Structure

No current template or renderer accepts parent/child organization nodes. The Ministry implementation must render a comprehensible hierarchy in HTML and may add an approved chart/download as a secondary form. Visual nesting without an accessible text relationship is insufficient.

### Search Results

The current Header dialog searches only service names rendered into the shell. It has no cross-content result record, result page, type filter, canonical query route or Ministry content index. The new generic results UI/contract belongs to shared capability; the Ministry adapter chooses and serializes product records. A production search engine is outside the V1 static UI implementation.

### News Listing

The current News section is explicitly bounded to Home and links to anchors in a generic content page. It does not satisfy chronological listing/detail semantics. Create one Ministry Editorial listing that is configured as News first and can support recommended Announcements without duplicating templates.

### Initiatives Listing

No current listing owns Initiative status, objectives or portfolio routes. Create a Ministry Portfolio listing whose controlled content type can later support Programs/Projects. Do not introduce a generic Foundation portfolio package in V1.

### Resources Library

The inventory's Documents section is planned and there is no current filterable resource/download library. Create a Ministry Resource library from existing controls, cards/lists and links. The record kind covers publication, report, policy, regulation and document; configured landing views reuse the same renderer later.

## 7. Shared Foundation Extensions

One required shared extension is approved by this mapping:

### Generic Search Results UI/contract

- **Owner:** shared capability, satisfying the UI/contract portion of deferred F13.
- **Inputs:** query; result records with title, URL, summary and content type; total; empty-state copy; optional filters/pagination.
- **Outputs:** semantic search form, result count/status, accessible results list and empty state.
- **Product boundary:** Ministry owns record extraction, searchable fields, type labels and the static demo index.
- **Integration boundary:** production crawling/indexing, ranking, analytics and remote search services remain external.
- **Header boundary:** replace or configure the service-only search action to reach the generic route; do not move service-catalogue filtering into general Search.

No other required type needs a shared Foundation change. Existing component qualification still applies at implementation time, but does not change ownership or REUSE/ADAPT classification.

### F12 decision

Deferred Table gap F12 is **not required** for Ministry V1 Resources. The approved records are a filterable card/list library with metadata and download actions. A table becomes justified only if a later dataset has meaningful column relationships that users must compare. Open Data is optional/later and does not make Table a current blocker.

## 8. Ministry-Owned Work

Ministry-owned implementation is limited to:

- page definitions and safe demo record schemas under the existing product boundary;
- Home composition and curated record mapping;
- Minister Profile and Organizational Structure templates;
- one Editorial listing/detail family for News, then recommended Announcements;
- one Portfolio listing/detail family for Initiatives, then recommended Programs/Projects;
- one Resource library/detail family with resource-kind configuration;
- Ministry Search index adapter and search route configuration;
- Ministry navigation/footer updates, product assets and external integration settings.

About, Strategy, Contact, FAQ and Services should be registered and configured, not forked. Product-specific classes may own page layout; intrinsic Foundation presentation remains with its canonical source.

## 9. Dependencies

All items depend first on a Ministry page registry/data-loading path in the product builder. Order numbers below are the recommended page-type implementation order after that boundary work.

| Order | Required type | Direct dependencies |
|---:|---|---|
| 1 | About Ministry | Product page definition; Heavy Content renderer; Page Intro/Breadcrumb |
| 2 | Strategy, Vision and Objectives | About/Heavy Content registration pattern; objectives content record |
| 3 | Contact | Product Contact data; existing Contact renderer; optional submit adapter contract |
| 4 | FAQ | Product question records; FAQ renderer; Contact route/CTA |
| 5 | Services Catalogue | Ministry service/category records; existing service renderer and product routes |
| 6 | Service Detail | Shared service records; catalogue route; operational URL policy |
| 7 | Minister Profile | Minister schema; approved portrait asset rules; product renderer registration |
| 8 | Organizational Structure | Hierarchy schema/validation; organization renderer; accessible fallback policy |
| 9 | Search Results | Shared Search/Results contract; all registered content domains; Ministry index adapter |
| 10 | News Detail | Editorial record schema; Heavy Content adaptation; canonical date/route rules |
| 11 | News Listing | Editorial records and detail renderer; listing empty state/filter policy |
| 12 | Initiative Detail | Portfolio record schema; Heavy Content adaptation; status vocabulary |
| 13 | Initiatives Listing | Initiative detail renderer; collection and empty-state rules |
| 14 | Resource Detail / Download | Resource schema; safe asset/URL metadata; Heavy Content adaptation |
| 15 | Resources Library | Resource details; kind/filter vocabulary; collection and empty-state rules |
| 16 | Home | Stable service, News, Initiative and Resource records/routes; Ministry section selection; product asset selection |

Pair record schemas are defined before either renderer. Detail precedes listing so every generated card can target an existing canonical route. Home comes last because it curates records from four completed families.

## 10. Recommended Implementation Sequence

1. **Product registry/data seam:** enable Ministry-owned page definitions and content inputs while retaining the compatibility build.
2. **Institutional family:** REUSE About and Strategy first to prove registration, then NEW Minister Profile and Organizational Structure.
3. **General family:** REUSE Contact and FAQ; implement the shared Search/Results contract and Ministry index adapter.
4. **Services family:** register the existing Catalogue and Detail with Ministry service/category records.
5. **Editorial family:** define one record schema, ADAPT News Detail, then build the NEW News Listing.
6. **Portfolio family:** define one Initiative record, ADAPT detail, then build the NEW listing.
7. **Resources family:** define file/resource metadata, ADAPT detail, then build the NEW library.
8. **Home composition:** assemble the completed families and select only the Home assets/runtimes needed.

The recommended first page implementation family is **Institutional**. About and Strategy provide low-risk proof of product registration before the Ministry-specific Minister and Organizational Structure work.

## 11. Risks / Decisions

| Risk / decision | Direction |
|---|---|
| Mapping versus production readiness | REUSE means contract fit, not that inventory `production_ready` changes. Each consumed component retains its documented qualification status. |
| Builder constraints | Current validation requires `index.html` and `services.html`, allows a fixed section set and derives service pages. Product page registration must be extended incrementally before new types can build; do not refactor unrelated renderers. |
| Home coupling | Search, Hero, carousel behavior and Home composition share `templates/government/home.js`, which is loaded globally. Ministry Home adaptation must select product/page behavior explicitly without reopening stabilized asset ownership. |
| Search scope | Generic UI and result semantics are shared; Ministry indexing is product-owned; production backend is integration-owned. Mixing these would create a false reusable contract. |
| Editorial ownership | News listing/detail stay Ministry-owned for V1. Announcements later configure the same family. Promotion waits for a second product. |
| Hierarchy accessibility | Organization Structure is HIGH risk because visual charts alone do not express relationships reliably. Textual hierarchy is required. |
| Resource safety | Download records need controlled HTTPS/local paths, format/size metadata, accessible labels and source/license ownership. File Upload is not a substitute. |
| Table F12 | Not required for the V1 resource list/detail contract. Keep deferred. |
| Heavy Content limits | Advanced rich media remains optional. News, Initiative and Resource details must work with current paragraphs/lists/links before any F11 work is considered. |
| Flat routes | Use current safe flat filenames for V1 mapping. Nested routing remains separate F09 work. |

## 12. Ready-for-Build Decision

**Decision: READY FOR SEQUENCED BUILD PLANNING.** The 16 required types now have explicit ownership, reuse classification, complexity, dependencies and order. Implementation should begin with the product registry/data seam and the Institutional family.

Readiness conditions for the first implementation task:

- scope one family at a time;
- preserve the legacy and product-boundary build commands;
- keep Foundation source canonical and avoid product copies;
- define records before renderers and use registered renderer IDs;
- treat Search as a separate shared-capability task with a Ministry adapter;
- keep backend integrations and optional/later types outside the first family;
- update the Ministry Blueprint/mapping only when implementation evidence changes a classification.

This decision does not authorize template creation in the mapping task itself.
