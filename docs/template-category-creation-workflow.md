# TEMPLATE CATEGORY CREATION WORKFLOW

## Purpose

Use this workflow whenever creating a NEW website template category.

Examples:

- Ministry Website
- University Website
- Municipality Website
- Government Services Portal
- Authority Website
- Hospital Website
- School Website
- Association Website

The goal is NOT to immediately build pages.

The goal is to first understand the real-world information architecture,
content needs, page types, user journeys, and presentation patterns of the
selected sector, then design a complete sellable product based on that research
while reusing the existing Platforms Code / DGA-compatible Foundation.

---

# STEP 1 — Ask for the Category Name

Ask only:

"What is the new template category?"

Example answer:

Ministry

---

# STEP 2 — Ask for Real Reference Websites

Ask the user to provide approximately 3–5 real websites from the same category.

Example:

"Please provide 4 real Ministry websites that should be used as references."

Important:

The websites do NOT need to use Platforms Code or DGA Design System.

At this stage the references are used mainly to study:

- information architecture
- content hierarchy
- page types
- navigation
- services
- institutional content
- media content
- programs and initiatives
- resources
- user journeys
- content presentation
- page relationships
- repeated patterns
- sector-specific needs

Do NOT evaluate only visual design.

Do NOT copy the reference websites.

Do NOT assume one website represents the whole sector.

---

# STEP 3 — Full Comparative Research

Analyze all provided websites.

For each reference, analyze at minimum:

## A. Information Architecture

- main navigation
- secondary navigation
- footer structure
- top-level categories
- nested page groups
- service taxonomy
- media taxonomy
- institutional taxonomy
- knowledge/resource taxonomy

## B. Page Inventory

Identify all meaningful page/content types.

Examples:

- Home
- About
- Leadership
- Organizational Structure
- Strategy
- Services Listing
- Service Detail
- News Listing
- News Detail
- Events
- Announcements
- Initiatives
- Programs
- Publications
- Reports
- Policies
- Open Data
- FAQ
- Contact
- Search
- etc.

## C. Page-Level Content Analysis

For important page types identify:

- page purpose
- primary user need
- page title pattern
- content hierarchy
- required content
- optional content
- section order
- CTAs
- metadata
- related content
- downloads
- filters
- search
- cards
- lists
- tables
- statistics
- media
- forms
- navigation behavior

## D. Homepage Analysis

Identify:

- hero purpose
- priority actions
- service discovery
- featured content
- news
- initiatives
- statistics
- institutional messaging
- audience segmentation
- calls to action
- footer priorities

## E. User Journeys

Identify common journeys such as:

- discover a service
- learn about the organization
- find leadership information
- read news
- download a publication
- discover an initiative
- search the site
- contact the organization

## F. Shared vs Sector-Specific Patterns

Classify findings into:

1. Shared website archetypes
2. Sector-specific page experiences
3. Optional / uncommon patterns
4. Outliers that should NOT become default product features

---

# STEP 4 — Synthesize the Category Model

Do NOT reproduce any single reference website.

Create an independent product model based on repeated and justified patterns.

For the selected category define:

## Category Identity

Example:

Product name:
Platforms Code — Ministry Website

Category:
Government / Ministry

## Product Information Architecture

Define the proposed final sitemap and content families.

## Page Families

Examples:

- Home
- Institutional
- Leadership
- Services
- Programs & Initiatives
- Media Center
- Resources & Knowledge
- Participation
- General / Utility

## Page Inventory

Classify each proposed page:

- REQUIRED V1
- RECOMMENDED V1
- OPTIONAL / LATER
- NOT REQUIRED

---

# STEP 5 — Define Every Page Properly

For every REQUIRED V1 page create a Page Specification.

Each Page Specification must include:

## Identity

- Page name
- Suggested Arabic title
- Suggested English title if relevant
- URL / route concept
- page family

## Purpose

- why the page exists
- main visitor need

## Content Model

- required fields
- optional fields
- repeatable fields
- relationships to other content

## Content Structure

- H1
- intro
- main sections
- supporting sections
- CTAs
- related content
- metadata

## Presentation

Explain HOW the content should be displayed.

Examples:

- hero
- cards
- split layout
- content blocks
- profile layout
- tabs
- accordion
- filters
- timeline
- stats
- download list
- data table
- hierarchy tree
- related content cards

## UX Behavior

- interactions
- filtering
- sorting
- pagination
- search
- empty states
- loading states if relevant

## Responsive Behavior

Describe expected mobile behavior.

Do not rely only on desktop composition.

## RTL

Specify RTL considerations.

## Accessibility

Define semantic and accessibility requirements.

## SEO

Define:

- title strategy
- description source
- heading hierarchy
- canonical behavior
- structured data if justified

## Components

List expected reusable Platforms Code / Foundation components.

## Ownership

Classify implementation as:

- shared Foundation capability
- category-specific template
- product configuration
- new reusable capability candidate

---

# STEP 6 — Create the Demo Organization

Create a fictional but realistic organization for the product demo.

Rules:

- never use a real organization identity
- never copy real institutional text
- content should sound professional and authentic
- all content across pages must belong to the SAME fictional organization
- strategy, services, initiatives, news, resources, leadership and statistics
  should be internally consistent

Example concept:

"Ministry of Community Development and Empowerment"

The organization should have:

- mission
- vision
- strategic priorities
- leadership
- services
- initiatives
- programs
- news
- resources
- reports
- contact information
- organizational units

---

# STEP 7 — Create Realistic Demo Content

Do NOT use placeholder content such as:

"Sample title"
"Lorem ipsum"
"Demo service"

Instead create realistic original content.

The content should:

- be sector appropriate
- be internally consistent
- demonstrate the page design
- exercise important components
- include short and long content
- include optional states where useful
- include meaningful labels and metadata

Content is original and inspired by identified needs,
not copied from references.

---

# STEP 8 — Map to Platforms Code

For every proposed page classify:

- REUSE
- ADAPT
- NEW

Determine which existing:

- components
- sections
- templates
- CSS
- utilities

can be reused.

Do not create duplicates.

Create new category-specific templates only when necessary.

---

# STEP 9 — Build Plan

Create implementation packages.

Recommended order:

1. product/data model
2. shared/simple pages
3. institutional pages
4. services
5. media
6. programs
7. resources
8. complex/high-risk pages
9. Home
10. integration
11. final QA

Each package must define:

- scope
- dependencies
- files
- renderer/template ownership
- validation
- exit criteria

---

# STEP 10 — Incremental Development

Build one package at a time.

Before implementing each page:

- consult the approved Page Specification
- reuse existing Foundation capabilities
- use approved demo content
- preserve product consistency

Do not design the page ad hoc during implementation.

## PAGE SPECIFICATION IMPLEMENTATION RULE

The approved product blueprint is the source of truth for page implementation.

Before implementing ANY page package, Codex MUST locate and read the complete
Page Specification for that page in the product blueprint.

The implementation must preserve the approved:

- page purpose
- user needs
- content model
- required fields
- optional fields
- content hierarchy
- section structure
- presentation method
- UX behavior
- mobile behavior
- RTL requirements
- accessibility requirements
- SEO requirements
- component expectations
- content relationships
- ownership rules

REUSE, ADAPT, and NEW describe the technical implementation strategy only.

They MUST NOT be used to simplify, reduce, or replace the approved page
experience.

For example:

REUSE does NOT mean:
"render the existing template with any compatible content."

REUSE means:
"reuse existing Foundation capabilities while still implementing the complete
approved Page Specification."

ADAPT means:
"compose or extend existing capabilities to satisfy the approved specification
without unnecessary duplication."

NEW means:
"create the smallest justified new capability required by the approved
specification."

If an existing Foundation component or template cannot represent an approved
page requirement, Codex must report the gap before silently omitting the
requirement.

Codex must NOT invent a different page structure during implementation unless
a proven technical constraint requires a change.

Any material deviation from the approved Page Specification requires explicit
approval before implementation.

The product blueprint remains the authoritative product/UX specification.
The build plan controls implementation order and package boundaries.
The existing-vs-new map controls reuse strategy.
The demo organization/content files control product demo content.

These documents have different responsibilities and must not override each
other.

---

# STEP 11 — Integration

After all V1 pages are complete:

- connect navigation
- connect internal links
- connect related content
- connect services
- connect news
- connect initiatives
- connect resources
- build Home from actual product content

The result must behave like one complete website,
not a collection of isolated page demos.

---

# STEP 12 — Final QA

Run broad QA only after integration.

Validate:

- responsive behavior
- RTL
- accessibility
- page hierarchy
- navigation
- internal links
- asset paths
- content consistency
- visual consistency
- browser behavior
- build output

---

# STEP 13 — Variants

Only after V1 is complete.

Decide which page types genuinely benefit from variants.

Examples:

- Home
- News
- Service
- About

Do NOT create variants only for cosmetic differences.

---

# STEP 14 — Product Packaging

Package as a sellable category product.

Include:

- demo website
- page inventory
- product manifest
- documentation
- configuration guidance
- reusable components
- templates
- assets
- sample content
- screenshots / preview later if required

---

# CRITICAL RULES

1. Research before implementation.
2. Use multiple real references.
3. Extract patterns; never copy websites.
4. Build a complete sector product, not random pages.
5. Page design must follow approved Page Specifications.
6. Demo content must be realistic, original, and internally consistent.
7. Reuse Platforms Code / DGA Foundation whenever possible.
8. Category-specific requirements may justify new templates.
9. Shared capabilities should not be duplicated inside products.
10. Home is built late, after its source content types exist.
11. Full QA is done at the final product stage.
12. Implementation must stop if product requirements are still undefined.
