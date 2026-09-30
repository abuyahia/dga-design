# Ministry Website V1 Blueprint

Status: planning baseline for the first commercial product. This document defines scope, contracts and build order only. It creates no page configuration, templates, content, assets or Foundation changes.

## 1. Executive Scope

Ministry Website V1 is an Arabic-first, RTL-ready static website product that presents the ministry, its leadership and strategy; publishes news and institutional resources; provides access to services; and supplies contact, FAQ and whole-site discovery. It is a reusable Ministry product definition, not one customer's finished site and not a CMS or transaction platform.

The proposed catalogue contains **32 page/content types**: **16 REQUIRED V1**, **8 RECOMMENDED V1**, and **8 OPTIONAL / LATER**. Three evaluated concepts are explicitly not separate pages in V1 because existing page families cover their purpose.

The product consumes the stabilized Foundation and current shared template capabilities. Ministry semantics stay under `products/ministry/`. No Foundation component is copied into the product, and no new shared abstraction is assumed before another product proves the same contract.

## 2. Ministry V1 Definition

The V1 release boundary is:

- all 16 REQUIRED V1 types are implemented and represented by safe fictitious demo records;
- shared shell, Header, Footer, Breadcrumb, Page Intro and existing reusable components remain canonical Foundation dependencies;
- Ministry-owned navigation, footer, page registry and demo content replace the transitional `site/government.json` dependency concern by concern;
- product-specific templates cover only Ministry semantics or first-product page families that are not yet proven shared;
- the package builds independently to `dist/products/ministry/` with no source dependency on another product;
- integrations such as form submission, service transactions and a production search index are explicit adapters rather than simulated backend services.

Priority meanings:

| Priority | Release meaning |
|---|---|
| REQUIRED V1 | Blocks the sellable V1 product if absent. |
| RECOMMENDED V1 | Belongs in the normal Ministry offer and should follow the required baseline, but does not block the first complete package. |
| OPTIONAL / LATER | Supported by a later product increment when a ministry has the content or operational need. |
| NOT NEEDED | Evaluated and deliberately represented by another page, taxonomy, module or navigation group. |

Route examples below use flat HTML filenames because that matches the current validated builder contract. Nested public routes can be considered only when configurable routing work is scheduled separately.

## 3. Information Architecture

```text
Home
├── The Ministry
│   ├── About the Ministry
│   ├── Minister
│   ├── Organizational Structure
│   ├── Strategy, Vision and Objectives
│   ├── Leadership                         [recommended]
│   └── Departments and Agencies           [recommended]
├── Services
│   ├── All Services
│   └── Service Detail
├── Media
│   ├── News
│   ├── Announcements                      [recommended]
│   └── Events                             [optional]
├── Initiatives and Programs
│   ├── Initiatives
│   └── Programs and Projects              [recommended]
├── Resources
│   ├── Publications and Reports
│   ├── Policies and Regulations
│   ├── Documents and Downloads
│   └── Open Data                          [optional]
├── Contact
├── FAQ
└── Search Results
```

Service categories are taxonomy/filter data in the catalogue. Related services are a module within Service Detail. Neither requires a separate page family in V1.

## 4. V1 Priority Classification

The 32 proposed types are counted in the table below.

| # | Page/content type | Area | Priority | Reason |
|---:|---|---|---|---|
| 1 | Home | Core | REQUIRED V1 | Establishes the Ministry proposition and routes users to priority tasks and content. |
| 2 | About Ministry | Core / Institutional | REQUIRED V1 | Explains mandate, responsibilities and institutional identity. |
| 3 | Minister Profile | Core / Institutional | REQUIRED V1 | A ministry requires an authoritative leadership entry distinct from a generic profile. |
| 4 | Organizational Structure | Core / Institutional | REQUIRED V1 | Makes hierarchy and responsibility discoverable in accessible text, with optional visual/download. |
| 5 | Strategy, Vision and Objectives | Strategy / Institutional | REQUIRED V1 | Provides the official strategic frame without overloading About. |
| 6 | Contact | Core / General | REQUIRED V1 | Supplies official channels and an integration-ready enquiry form. |
| 7 | FAQ | Core / General | REQUIRED V1 | Answers recurring questions and reduces support demand. |
| 8 | Search Results | Core / Discovery | REQUIRED V1 | A complete multi-domain ministry site needs whole-site discovery beyond service-only search. |
| 9 | News Listing | Media | REQUIRED V1 | Provides the canonical chronological news index. |
| 10 | News Detail | Media | REQUIRED V1 | Gives each item a stable, shareable and accessible article page. |
| 11 | Services Catalogue | Services | REQUIRED V1 | Central entry to services, categories and audience filtering. |
| 12 | Service Detail | Services | REQUIRED V1 | Communicates requirements, steps, documents and operational destinations. |
| 13 | Initiatives Listing | Strategy / Programs | REQUIRED V1 | Ministries need a structured view of active and completed initiatives. |
| 14 | Initiative Detail | Strategy / Programs | REQUIRED V1 | Provides objectives, status, ownership and outcomes for an initiative. |
| 15 | Resources Library | Resources | REQUIRED V1 | One searchable/filterable collection covers publications, reports, policies, regulations and downloads. |
| 16 | Resource Detail / Download | Resources | REQUIRED V1 | Supplies metadata, context and an accessible download or external destination. |
| 17 | Announcements Listing | Media | RECOMMENDED V1 | Time-sensitive notices are common but can follow the core News release. |
| 18 | Announcement Detail | Media | RECOMMENDED V1 | Supports stable notice URLs and expiry/status information. |
| 19 | Programs / Projects Listing | Strategy / Programs | RECOMMENDED V1 | Separates sustained programs/projects from bounded initiatives when the ministry uses both. |
| 20 | Program / Project Detail | Strategy / Programs | RECOMMENDED V1 | Provides scope, timeline, owner and progress for each program/project. |
| 21 | Leadership Directory | Institutional | RECOMMENDED V1 | Supports deputy ministers and senior leadership without changing the Minister contract. |
| 22 | Departments / Agencies Directory | Institutional | RECOMMENDED V1 | Helps users understand units and affiliated bodies when that structure exists. |
| 23 | Publications / Reports Landing | Resources | RECOMMENDED V1 | A configured Resources Library view gives prominent access without a new template. |
| 24 | Policies / Regulations Landing | Resources | RECOMMENDED V1 | A configured Resources Library view separates authoritative legal content. |
| 25 | Events Listing | Media | OPTIONAL / LATER | Needed only when the ministry runs a sustained public events programme. |
| 26 | Event Detail | Media | OPTIONAL / LATER | Added with Events Listing when dates, venues or registration justify individual pages. |
| 27 | Leadership Profile | Institutional | OPTIONAL / LATER | Individual profiles beyond the Minister depend on ministry publishing policy. |
| 28 | Department / Agency Detail | Institutional | OPTIONAL / LATER | A directory record is sufficient until units need substantial independent content. |
| 29 | Open Data Landing | Resources | OPTIONAL / LATER | Requires governance, datasets and update commitments beyond a static placeholder. |
| 30 | Partners | Institutional | OPTIONAL / LATER | A dedicated page is useful only with approved partner data and relationships. |
| 31 | Statistics | Institutional | OPTIONAL / LATER | Publish only when metrics have defined sources, dates and owners. |
| 32 | Achievements | Strategy / Institutional | OPTIONAL / LATER | Can initially be expressed through strategy outcomes, initiatives and verified statistics. |

Evaluated exclusions, not included in the count:

- **Media Center landing — NOT NEEDED:** the Media navigation group can link directly to News, Announcements and optional Events.
- **Service Category landing — NOT NEEDED:** category is required taxonomy in Services Catalogue; a standalone route would duplicate the filtered catalogue.
- **Digital Channels / Social page — NOT NEEDED:** approved channels belong in Header utilities, Contact and Footer unless they acquire substantial independent content.

## 5. Template Families

| Family | Page/content types | Ownership direction |
|---|---|---|
| Shell and Home Composition | Home | Ministry composition using the shared government shell and Foundation sections. |
| Institutional Content | About Ministry; Strategy, Vision and Objectives; Organizational Structure | Heavy Content handles prose pages; Organization needs a Ministry-specific structure template. |
| Leadership and Directory | Minister; Leadership Directory/Profile; Departments/Agencies Directory/Detail | Ministry-specific semantics composed from Page Intro, Avatar/Card, links and content primitives. |
| Editorial Media | News and Announcement listing/detail; optional Events | One product-owned listing/detail family with content-kind configuration, not a template per label. |
| Services | Services Catalogue and Service Detail | Reuse the existing shared service capability and Service Card; product supplies data and routes. |
| Portfolio | Initiatives and Programs/Projects listing/detail | One Ministry-owned listing/detail family with a type field and controlled status vocabulary. |
| Resources | Resources Library, configured landings and Resource Detail | One product-owned library/detail family with publication/report/policy/regulation/document kinds. |
| Discovery and Interaction | Search Results, Contact and FAQ | Reuse Contact/FAQ; extend shared search and provide a Ministry index adapter. |

## 6. Required Page Contracts

### Shell, institutional and leadership

| Required type | Purpose, route and pair | Required content fields | Optional content fields | Foundation reuse and Ministry work |
|---|---|---|---|---|
| Home | Product entry; `index.html`; no detail pair | `title`, `hero.title`, `hero.summary`, `hero.primary_action`, ordered section configuration, featured service IDs, latest news IDs | hero secondary action/media, initiative IDs, announcement IDs, resource IDs, statistics, partners | Reuse shell, Header, Footer, Hero candidate, Card, Service Card, Button, Link, shared section primitives and Feedback. Ministry owns section selection/order and home data mapping. |
| About Ministry | Mandate and identity; `about.html`; no pair | `title`, `summary`, `mandate`, `responsibilities`, `updated` | history, establishment basis, image, attachments, related links | Reuse Page Intro, Breadcrumb, Heavy Content, TOC, List, Link and Feedback. Product integration only. |
| Minister Profile | Authoritative minister page; `minister.html`; standalone leadership type | `name`, `official_title`, `portrait`, `portrait_alt`, `biography`, `updated` | message, appointment date, qualifications, experience, speeches, approved social links | Reuse Page Intro, Breadcrumb, Avatar or image primitives, Heavy Content, Link and Feedback. Ministry-specific profile template and data contract required. |
| Organizational Structure | Accessible hierarchy; `organization.html`; no pair | `title`, `summary`, ordered hierarchy nodes with unique IDs, node labels and parent relationships, `updated` | node descriptions, approved organization chart image with alt text, downloadable accessible document | Reuse Page Intro, Breadcrumb, Card/List/Link/Button and Feedback. Ministry-specific hierarchy template must keep a textual representation available. |
| Strategy, Vision and Objectives | Strategic frame; `strategy.html`; no pair | `title`, `summary`, `vision`, `mission`, ordered objectives, `updated` | strategic pillars, KPIs with source/date, timeline, documents, related initiatives | Reuse Page Intro, Breadcrumb, Heavy Content, TOC, List, Link and Feedback. Product configuration only unless structured KPI blocks are later required. |

### General discovery and interaction

| Required type | Purpose, route and pair | Required content fields | Optional content fields | Foundation reuse and Ministry work |
|---|---|---|---|---|
| Contact | Official support and enquiry; `contact.html`; no pair | page title/description, contact categories, official channels, field labels/names, required state, privacy/help text | location, hours, social channels, attachment policy, backend adapter | Reuse the existing Contact template, Page Intro, form controls, File Upload, Card, Button and Feedback. Ministry config supplies content; production submission remains an adapter. |
| FAQ | Common answers; `faq.html`; no pair | page title/description and questions with unique `id`, `question`, `answer` | category, related link, Contact CTA | Reuse Page Intro, Breadcrumb, FAQ, canonical Accordion, Contact CTA and Feedback. Product configuration only. |
| Search Results | Whole-site results; `search.html?q=...`; no listing/detail pair | query, total, result records with `title`, `url`, `summary`, `content_type`, empty state | type filter, date, pagination, spelling suggestion, highlighted terms | Reuse Header search trigger where suitable, Page Intro, Text Input, Button, Link, Card/List, Tag and existing Pagination after qualification. Shared Search/Results capability plus Ministry index adapter is required. |

### Media

| Required type | Purpose, route and pair | Required content fields | Optional content fields | Foundation reuse and Ministry work |
|---|---|---|---|---|
| News Listing | Chronological index; `news.html`; pairs with News Detail | page title/description; records with `id`, `title`, `summary`, `published_at`, detail route | category, thumbnail/alt, tags, featured flag, pagination | Reuse Page Intro, Breadcrumb, Card, Tag, Link, Button and Feedback. Current News section is a bounded home grid; Ministry needs a product listing template. |
| News Detail | Shareable article; `news-<slug>.html`; pairs with News Listing | `id`, `title`, `published_at`, body blocks, canonical route, `updated` | lead image/alt, author, category, tags, attachments, related news | Reuse Page Intro/Breadcrumb or article heading composition, Heavy Content blocks, Link, Tag and Feedback. Ministry editorial-detail template required; optional rich media must respect deferred media limits. |

### Services

| Required type | Purpose, route and pair | Required content fields | Optional content fields | Foundation reuse and Ministry work |
|---|---|---|---|---|
| Services Catalogue | Find and filter services; `services.html`; pairs with Service Detail | page title/description; services with unique `id`, `title`, `description`, categories, audiences and detail route | featured flag, channel, owner, query/filter state | Reuse Page Intro, Service Card, Text Input, Tag, Button and the existing Service Catalogue capability. Product supplies taxonomy and records. |
| Service Detail | Explain and start a service; `service-<slug>.html`; pairs with catalogue | current contract fields: `id`, `title`, `description`, `audiences`, `steps`, `requirements`, `documents` | duration, channels, cost, owner, languages, agreement, FAQs, start/guide/video/support URLs, apps, related service IDs, updated date | Reuse the existing Service Detail template, Page Intro, Breadcrumb, Tabs, Lists, Buttons, Service Card, rating and Feedback. Transaction endpoints remain integration-owned. |

### Initiatives and resources

| Required type | Purpose, route and pair | Required content fields | Optional content fields | Foundation reuse and Ministry work |
|---|---|---|---|---|
| Initiatives Listing | Browse ministry initiatives; `initiatives.html`; pairs with Initiative Detail | page title/description; records with `id`, `title`, `summary`, controlled `status`, detail route | start/end dates, owner, thumbnail/alt, featured flag, category | Reuse Page Intro, Breadcrumb, Card, Tag, Link, Button and Feedback. Ministry Portfolio listing template required. |
| Initiative Detail | Explain goals and outcomes; `initiative-<slug>.html`; pairs with listing | `id`, `title`, `summary`, objectives, status, owner, body blocks, canonical route, `updated` | dates, progress, verified metrics, partners, documents, media, related initiatives/programs | Reuse Page Intro, Breadcrumb, Heavy Content, Lists, Tag, Link and Feedback. Ministry Portfolio detail template required. |
| Resources Library | Find institutional resources; `resources.html`; pairs with Resource Detail | page title/description; records with `id`, `title`, controlled `kind`, published/updated date, format, detail/download destination | owner, language, file size, category, summary, filters, pagination | Reuse Page Intro, Breadcrumb, Text Input, Select, Card/List, Tag, Link, Button and Feedback. Ministry Resource library template required. |
| Resource Detail / Download | Explain and expose one resource; `resource-<slug>.html`; pairs with library | `id`, `title`, `kind`, summary, published/updated date, format, accessible file or HTTPS URL, canonical route | cover/alt, version, owner, language, file size, body blocks, related resources | Reuse Page Intro, Breadcrumb, Heavy Content, List, Link/Button and Feedback. Ministry Resource detail template and download metadata contract required. |

## 7. Home Page Composition

This is section order and presence only; it does not prescribe visual layout.

| Order | Section | Presence | Configuration rule |
|---:|---|---|---|
| 1 | Hero | REQUIRED | Configurable ministry title, value statement, primary route and approved media; no automatic claims or destinations. |
| 2 | Priority Services | REQUIRED | Configurable selection from the canonical service collection using Service Card. |
| 3 | About the Ministry summary | REQUIRED | Short mandate summary and link to About; long institutional copy remains off Home. |
| 4 | Featured Initiatives | REQUIRED | Configurable selection from Initiative records; section hides only when the product has no publishable records during setup. |
| 5 | Latest News | REQUIRED | Configurable count and featured selection from News; all items link to News Detail. |
| 6 | Announcements | CONFIGURABLE / RECOMMENDED | Enabled when Announcement records exist; uses the Editorial family. |
| 7 | Publications and Resources | CONFIGURABLE / RECOMMENDED | Curated Resource records with a link to the library. |
| 8 | Key Statistics | OPTIONAL | Requires value, label, source and effective date for every metric. |
| 9 | Partners | OPTIONAL | Requires approved name, relationship and accessible logo/label data. |
| 10 | Contact CTA | REQUIRED | Routes to Contact and uses the shared CTA composition where its contract fits. |
| 11 | Page Feedback | REQUIRED | Uses the shared preview/integration contract and must not imply backend submission without an adapter. |

Header, Digital Stamp and Footer belong to the shell and are not Home sections.

## 8. Navigation Blueprint

Keep primary navigation to two levels, matching the current Navigation Header disclosure contract.

| Main item | Second-level links |
|---|---|
| Home | Direct route only |
| The Ministry | About Ministry; Minister; Organizational Structure; Strategy, Vision and Objectives; Leadership and Departments when enabled |
| Services | All Services; optionally a small curated set of category-filtered catalogue links |
| Media | News; Announcements when enabled; Events when enabled |
| Initiatives and Programs | Initiatives; Programs and Projects when enabled |
| Resources | Resources Library; Publications and Reports; Policies and Regulations; Open Data when enabled |
| Contact | Direct route; FAQ may sit here or in utilities depending on available header width |

Utility actions:

- whole-site Search;
- language switch only when an actual translated product build exists;
- accessibility link;
- Digital Stamp in the shared shell;
- service login or e-services portal only when a real approved destination exists.

Avoid a third navigation level. Category pages should normally be catalogue filter states rather than nested menu trees.

## 9. Footer Blueprint

| Group | Content |
|---|---|
| Institutional | About Ministry; Minister; Organizational Structure; Strategy; Leadership/Departments when enabled |
| Services | All Services; selected service categories or priority services; service support destination |
| Media and Programmes | News; Announcements; Initiatives; Programs/Projects; optional Events |
| Resources | Publications and Reports; Policies and Regulations; Documents/Downloads; optional Open Data |
| Policies / Legal | Privacy and Terms; Accessibility; site map if introduced; content-use or legal notices supplied by the ministry |
| Contact | Contact page; FAQ; official address, phone or email where approved |
| Digital Channels | Approved social and digital channels only; each needs a label and real URL |

The footer also carries the product's disclaimer/copyright, content update statement where applicable, and approved logos. Footer configuration owns this data; the Foundation Footer owns structure and presentation.

## 10. Foundation Reuse Map

| Required V1 page(s) | Existing reusable assets |
|---|---|
| Home | Government shell, Digital Stamp, Navigation Header, Footer, container/layout primitives, current Hero composition as a candidate, Service Card, Card, Button, Link, home Services/News compositions where contracts fit, Contact CTA, Feedback |
| About Ministry | Page Intro, Breadcrumb, Heavy Content, Table of Contents, Divider, List, Link, Feedback |
| Minister Profile | Page Intro, Breadcrumb, Avatar candidate, Card, Heavy Content blocks, Link, Feedback |
| Organizational Structure | Page Intro, Breadcrumb, Card, List, Link, Button, Feedback |
| Strategy, Vision and Objectives | Page Intro, Breadcrumb, Heavy Content, Table of Contents, List, Link, Feedback |
| Contact | Existing Contact template/section, Page Intro, Breadcrumb, Card, Label, Text Input, Select, Textarea, File Upload, Button, Feedback |
| FAQ | Page Intro, Breadcrumb, FAQ section, canonical Accordion, Contact CTA, Feedback |
| Search Results | Navigation Header search entry, Page Intro, Breadcrumb, Label, Text Input, Select, Button, Link, Card/List, Tag, Pagination candidate, Feedback |
| News Listing / Detail | Page Intro, Breadcrumb, Card, Tag, Link, Button, Heavy Content blocks, List, Feedback; current News grid only for bounded Home use |
| Services Catalogue / Detail | Existing shared service templates/sections, Page Intro, Breadcrumb, Service Card, Text Input, Tag, Tab, List, Button, Link, rating and Feedback |
| Initiatives Listing / Detail | Page Intro, Breadcrumb, Card, Tag, Link, Button, Heavy Content blocks, List, Feedback |
| Resources Library / Detail | Page Intro, Breadcrumb, Text Input, Select, Card/List, Tag, Link, Button, Heavy Content, Table of Contents where useful, Feedback |

Items marked candidate remain subject to their existing inventory status. Reuse does not promote `production_ready` or bypass page-level acceptance.

## 11. Ministry-Specific Capabilities

The following remain under `products/ministry/` for V1:

- Ministry Home composition and mapping of curated services, news, initiatives and resources;
- Minister Profile template and record contract;
- accessible Organizational Structure template and hierarchy data;
- Editorial listing/detail family for News and Announcements, with optional Events later;
- Portfolio listing/detail family for Initiatives and Programs/Projects;
- Resource library/detail family and Ministry resource taxonomy;
- Leadership and Departments/Agencies directories and details when scheduled;
- Ministry page registry, navigation, footer, demo records and product-owned media;
- adapters for the Ministry whole-site search index, enquiry submission and service destinations.

These capabilities may compose Foundation assets. They are not promoted merely because another sector could look visually similar.

## 12. Gaps / New Work Required

Only gaps needed to deliver the REQUIRED V1 scope are listed as blockers below.

| Gap | Classification | Required response |
|---|---|---|
| Ministry page registry and split demo data | Product integration only | Replace the transitional page/content portion of `site/government.json` with validated product-owned definitions incrementally. Keep navigation/footer ownership already implemented. |
| Ministry Home composition | Product-specific template needed | Register a Ministry Home composition that consumes canonical sections; do not fork the shared shell or Foundation components. |
| Minister Profile | Product-specific template needed | Define the minister record and a semantic profile template composed from Page Intro and shared content primitives. |
| Organizational Structure | Product-specific template needed | Define hierarchy data and an accessible textual rendering; visual/download forms are optional enhancements. |
| Whole-site Search / Results | Shared capability extension needed | Schedule deferred F13 because Search is REQUIRED V1. Build a sector-neutral results contract; keep indexing/content selection in the Ministry adapter. |
| News listing/detail | Product-specific template needed | Build one editorial family. Reuse the current bounded News grid only on Home; do not treat it as a complete listing. |
| Initiatives listing/detail | Product-specific template needed | Build one Portfolio family whose controlled type can later support Programs/Projects. |
| Resources library/detail | Product-specific template needed | Build one filterable library/detail family from Foundation controls/cards/links; keep publication/report/policy/document distinctions in data. |
| About and Strategy | Product integration only | Configure existing Page Intro and Heavy Content capability with separate records/routes. |
| Contact and FAQ | Product integration only | Register existing shared templates and product content. Backend submission remains an explicit adapter. |
| Services Catalogue and Detail | Product integration only | Register the existing shared service capability against Ministry service/category records and operational URLs. |

No other deferred Foundation P2 item is a V1 blocker. F06, F07, F08, F09, F11 and F12 remain deferred unless a concrete page implementation later proves otherwise.

## 13. Deferred Features

The following do not block Ministry V1:

- Events Listing and Event Detail;
- individual Leadership Profiles beyond the Minister;
- Department / Agency Detail;
- Open Data landing and dataset workflows;
- dedicated Partners, Statistics and Achievements pages;
- rich media galleries and advanced Heavy Content media;
- advanced faceted search, search suggestions and external search services beyond the required results contract;
- nested route architecture, multilingual content builds and customer/tenant overlays;
- backend contact submission, service transactions, analytics and content-management integration;
- alternative A/B page variants and a generic variant engine.

Announcements, Programs/Projects, Leadership and Department directories, plus configured Resource landings are recommended follow-on V1 increments rather than exit blockers.

## 14. Recommended Build Order

1. **Product configuration foundation:** define the Ministry page registry and demo-data schemas; keep all data fictitious and preserve the current compatibility build during migration.
2. **Shell and institutional family:** register shared shell, About and Strategy; build Ministry Home, Minister Profile and Organizational Structure.
3. **General discovery and interaction:** register Contact and FAQ; implement shared Search/Results plus the Ministry index adapter.
4. **Editorial media family:** implement News listing/detail, then add Announcements by configuration of the same family.
5. **Services family:** bind Ministry categories and records to the existing Services Catalogue and Service Detail capability.
6. **Portfolio family:** implement Initiatives listing/detail, then enable Programs/Projects through the same family.
7. **Resources family:** implement Resources Library/Detail, then configure Publications/Reports and Policies/Regulations landings.
8. **Recommended and optional modules:** add directories, Events, Open Data, Partners, Statistics or Achievements only with approved content and a product need.
9. **Product release:** verify routes, package only resolved dependencies, complete product-level accessibility/responsive/RTL validation, and publish the independent `dist/products/ministry/` artifact.

Each family should complete its data contract, template composition, focused tests and product registry entry before the next family starts. Shared promotion follows the cross-product rule after a second proven consumer.

## 15. Exit Criteria for Ministry V1

Ministry Website V1 is complete when:

- all 16 REQUIRED V1 page/content types build from product-owned definitions and safe demo data;
- every internal page has one H1, a canonical Page Intro where compatible, and a variable-depth Breadcrumb;
- Header/Footer use Ministry-owned configuration while their source remains Foundation-owned;
- required listing/detail relationships, canonical routes, empty states and related links resolve;
- whole-site Search returns the registered Ministry content domains and exposes an accessible empty state;
- Contact, service starts/downloads and Feedback state clearly distinguish preview behavior from real adapters;
- Ministry-specific templates contain no copied Foundation component, section, partial, style or runtime;
- required assets have source/alt/license metadata and the generated package contains only resolved Foundation/shared/product assets;
- page configuration and demo content no longer rely on the transitional site file for migrated concerns;
- focused unit/build checks, product-wide static validation, responsive RTL/LTR review, keyboard/accessibility review and the approved product browser matrix pass at the release stage;
- the package builds with `python3 scripts/build_site.py --product ministry` to `dist/products/ministry/` and runs independently;
- recommended/optional omissions are documented and do not leave broken navigation or empty placeholders;
- Foundation v1.0 status and resolved F01, F02, F03, F04, F05 and F10 remain unchanged.
