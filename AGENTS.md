# Government Templates — Codex Master Workflow

## 1. Project Mission

This repository is a reusable government design system and template library.

The goal is NOT to create isolated HTML pages.

The goal is to continuously build a reusable system composed of:

1. Design tokens and shared foundations
2. Reusable UI components
3. Shared layout structures
4. Reusable content sections
5. Page archetypes
6. Complete page templates
7. Sector-specific template kits

Every new template should reuse as much of the existing system as possible.

As the library grows, every new template should require fewer new components and less duplicated CSS.

The implementation must remain independent from:

- Drupal
- Next.js
- React
- Vue
- Bootstrap
- Tailwind
- Any other framework or CMS

Unless a future task explicitly requests an integration layer.

---

# 2. Primary Architecture

Always think in this hierarchy:

```text
Design Tokens
    ↓
Base / Shared Styles
    ↓
Core Components
    ↓
Composite Components
    ↓
Reusable Sections
    ↓
Page Archetypes
    ↓
Templates
    ↓
Sector Kits
```

Templates should primarily be composition.

Avoid implementing page-specific HTML or CSS when the same result can be achieved using reusable project assets.

---

# 3. Golden Reuse Principle

Always follow this decision path:

```text
EXISTING COMPONENT
        ↓
      REUSE
```

If there is no exact match:

```text
EQUIVALENT COMPONENT
        ↓
SAFE VARIANT / EXTENSION
```

If no suitable reusable implementation exists:

```text
REFERENCE
   ↓
CREATE NEW REUSABLE COMPONENT
```

Then:

```text
COMPONENTS
    ↓
SECTIONS
    ↓
TEMPLATE
    ↓
INTEGRATION
    ↓
VALIDATION
```

Never recreate something that already exists.

Never copy an existing component and rename it simply because the new template requires a minor variation.

---

# 4. Interactive Command

When the user says:

```text
أضف قالب
```

or:

```text
Add Template
```

start the Interactive Template Builder workflow.

Do NOT:

- Immediately scan the entire repository
- Immediately start coding
- Ask for all references in one large question
- Make assumptions about the template
- Rebuild architecture already present in the project

Collect the information progressively.

---

# 5. Step 1 — Template Name

Ask only:

> ما اسم القالب المطلوب إنشاؤه؟

Wait for the answer.

Then continue to Step 2.

---

# 6. Step 2 — DGA Reference

Ask:

> أرسل رابط قالب DGA إن وجد، أو اكتب Skip إذا لم يوجد.

Use the DGA reference primarily to understand:

- Official government template type
- Expected page structure
- Standard sections
- Government UX conventions
- Content hierarchy
- General government design expectations

DGA should NOT automatically override a more precise Figma visual specification.

Wait for the answer.

Then continue.

---

# 7. Step 3 — Figma Reference

Ask:

> أرسل رابط Figma الخاص بالقالب أو الـNode المطلوب، أو اكتب Skip إذا لم يوجد.

When available, Figma is the PRIMARY visual source of truth.

Use Figma to understand:

- Layout
- Dimensions
- Grid
- Spacing
- Typography
- Font weights
- Colors
- Borders
- Radius
- Alignment
- Icons
- Component states
- Responsive behavior
- RTL behavior
- Visual hierarchy
- Section relationships

Do not approximate a component when its actual Figma specification is available.

Wait for the answer.

Then continue.

---

# 8. Step 4 — Live Production Reference

Ask:

> أرسل رابط صفحة حقيقية منشورة تستخدم هذا النوع من القالب، إن وجدت، أو اكتب Skip.

Examples:

- KKU
- Government websites
- Universities
- Authorities
- Ministries
- Existing production implementations
- Other approved references

Use the live page primarily to understand:

- Real content
- Content hierarchy
- Functional behavior
- User journeys
- Actual data presentation
- Interaction patterns
- Real-world edge cases

Do NOT blindly copy production HTML or CSS.

Use the project's design system for the implementation.

---

# 9. Reference Priority

Use each reference according to its purpose.

## Visual Design

```text
Figma
  ↓
DGA
  ↓
Live Page
```

## Template Structure

```text
DGA
  ↓
Figma
  ↓
Live Page
```

## Real Content and Behavior

```text
Live Page
  ↓
DGA
  ↓
Figma
```

## Implementation

```text
Existing Project
      ↓
Existing Components
      ↓
Existing CSS / Tokens
      ↓
Safe Extension
      ↓
New Component
```

If references conflict:

Do not silently guess.

Use the reference appropriate to the specific decision.

Ask the user only when the conflict materially affects implementation.

Ask ONE concise question.

---

# 10. Minimum Reference Requirement

Not every reference is mandatory.

Valid combinations may include:

- DGA + Figma + Live Page
- DGA + Figma
- Figma + Live Page
- DGA + Live Page
- Figma only
- Another sufficiently precise reference

Do not block implementation merely because one reference type is missing.

However, do not begin implementation if the available references are insufficient to understand the template accurately.

If information is missing, request only the specific missing reference.

---

# 11. Step 5 — Template Analysis

After collecting enough references, analyze the target template before writing code.

Identify:

- Main page purpose
- Page structure
- Sections
- Components
- Content blocks
- Breadcrumb
- Page header
- Hero
- Cards
- Lists
- Forms
- Tables
- Tabs
- Accordions
- Alerts
- CTAs
- Related content
- Feedback sections
- Sidebars
- Attachments
- Navigation relationships
- Interactive elements
- Responsive requirements
- RTL requirements
- Accessibility requirements
- Template-specific elements

Create an implementation map internally.

Do NOT start by writing HTML.

First understand what the template is made of.

---

# 12. Step 6 — Component Registry

Before performing repository-wide searches, check:

```text
docs/component-registry.md
```

This file is the primary reusable component inventory.

The registry should contain, when applicable:

- Component name
- Purpose
- Source / HTML location
- CSS location
- JavaScript location
- Variants
- Templates using it
- Important implementation notes

If the registry says a component exists:

Inspect only the relevant implementation files when necessary.

Do not broadly search the entire repository unless the registry information is incomplete, outdated, or incorrect.

---

# 13. Missing Component Registry

If:

```text
docs/component-registry.md
```

does not exist:

Create it.

Inspect only reusable components relevant to the current template.

Register them.

Do NOT perform a full repository audit simply to populate the registry.

The registry must grow incrementally as the system grows.

---

# 14. Step 7 — Component Audit

For each required element classify it as:

### A. EXISTING — REUSE

Use the component without duplicating it.

### B. EXISTING — SAFE VARIANT / EXTENSION

Extend the current component in a reusable and backward-compatible way.

### C. MISSING — CREATE

Create a new reusable component only when no suitable implementation exists.

Typical reusable assets include:

- Header
- Footer
- Navigation
- Breadcrumb
- Page Header
- Buttons
- Icon buttons
- Inputs
- Textareas
- Selects
- Checkboxes
- Radio buttons
- File upload
- Cards
- Alerts
- Accordions
- Tabs
- Pagination
- Lists
- Tables
- Feedback component
- Related links
- Containers
- Layout helpers
- Grid helpers
- Typography utilities
- Spacing utilities

Never create a new component before checking A and B.

---

# 15. Reuse Rule

Do NOT recreate:

- Existing HTML structures
- Existing CSS blocks
- Existing JavaScript behavior
- Existing components
- Existing sections
- Header
- Footer
- Navigation
- Breadcrumb
- Shared utilities
- Existing design tokens

Do NOT duplicate CSS unnecessarily.

Prefer composition.

Prefer variants.

Prefer extension.

Prefer existing patterns.

---

# 16. Safe Extension Rule

If an existing component can support the requirement through a small reusable extension:

Extend it.

Example:

Existing:

```text
Card
```

Required:

```text
Card with optional icon
```

Preferred:

```text
Card
+ reusable icon variant
```

Avoid:

```text
IconCard
AnotherCard
SpecialPageCard
UniversityIconCard
```

when the structural difference is minor.

However:

Do NOT turn a simple component into an overly complex universal component.

Create a separate component when:

- Semantics are meaningfully different
- Structure is substantially different
- Behavior is substantially different
- Accessibility requirements differ
- Reuse would make the existing component fragile or confusing

---

# 17. Composite Components

Before treating an element as a full page section, consider whether it belongs to the composite component layer.

Examples:

- Service Card
- News Card
- Event Card
- Profile Card
- Statistic Item
- Document Card
- Contact Card
- Location Card
- Quick Link
- Search Result Item
- Metadata List
- Related Content Item
- Filter Group
- Empty State
- Download Item

Composite components should be built from existing core components where possible.

---

# 18. Reusable Sections

Templates should reuse sections rather than repeatedly implementing section structures.

Examples:

- Hero
- Page Intro
- Featured Services
- Services Grid
- Latest News
- News Grid
- Events
- Statistics
- Leadership
- Quick Links
- Featured Programs
- Featured Initiatives
- Documents
- Publications
- FAQ
- Related Content
- Contact Information
- Locations
- CTA
- Partners
- Media Gallery
- Feedback

A section should be reusable across sectors whenever its behavior and content structure are equivalent.

Avoid:

```text
university-news-grid
ministry-news-grid
authority-news-grid
```

when all three can use:

```text
news-grid
```

with variants or data differences.

---

# 18A. PAGE INTRO RULE

Always reuse the existing Page Intro section for internal-page heading areas.

Do not create a new page-title, hero-title, breadcrumb-header, or intro section if the requirement can be handled by an existing Page Intro variant.

Default behavior:

- If the provided reference does not clearly define the breadcrumb/title region, use the default Page Intro variant.
- Reuse the existing Breadcrumb component through `breadcrumb_markup`.
- Use `description` when introductory text is required.
- Use `compact` for dense/internal pages.
- Use `featured` when an additional block visually belongs to the intro area.
- Use `decorative` only when a background/pattern is genuinely part of the intended visual design.

Create a new Page Intro variant only when none of the existing variants can represent the required structure cleanly.

---

# 19. Variants Rule

When differences are primarily visual or presentational, prefer variants.

Example:

```text
Hero
├── standard
├── image
├── split
└── search-led
```

Avoid creating:

```text
university-hero
ministry-hero
authority-hero
```

unless their structure or behavior is genuinely different.

Use the same principle for:

- Cards
- Page headers
- Services
- News
- Events
- Statistics
- CTA
- Directories
- Listings
- Forms

---

# 20. Page Archetype Awareness

Before creating a completely new page layout, check whether the template fits an existing page archetype.

Common archetypes include:

1. Homepage
2. Landing Page
3. Standard Content Detail
4. Rich Content Detail
5. Listing
6. Filtered Listing
7. Directory
8. Profile
9. Service Detail
10. Process / Journey
11. Timeline
12. Document / Regulation
13. Data / Statistics Dashboard
14. Map / Location
15. Form / Interaction
16. Search Results

For example:

```text
Academic Program Detail
Government Initiative Detail
Medical Specialty Detail
```

may all share the same underlying Rich Content Detail archetype.

Do not automatically create a new layout for every business concept.

---

# 21. Step 8 — Missing Component Creation

If a required reusable element is missing:

1. Confirm no existing or equivalent component exists.
2. Review the appropriate reference.
3. Prefer the exact Figma component/node when available.
4. Understand structure.
5. Understand states.
6. Understand responsive behavior.
7. Understand RTL behavior.
8. Understand accessibility needs.
9. Create the reusable component.
10. Create only the CSS required for that component.
11. Add JavaScript only if behavior requires it.
12. Follow existing naming conventions.
13. Follow existing project architecture.
14. Use existing tokens and utilities.
15. Register the new component in `docs/component-registry.md`.

Do NOT create page-specific markup when the element belongs in the reusable component system.

---

# 22. Additional Reference Requests

Do NOT ask for more references unless required.

If one specific element cannot be implemented accurately:

1. Stop only the affected part.
2. Continue all work that can safely proceed.
3. Explain exactly what is unclear.
4. Ask for ONE specific missing reference.
5. Prefer the exact Figma node or relevant real page.
6. Continue from the same implementation stage after receiving it.

Do not restart the analysis.

Example:

> مكوّن رفع الملفات غير واضح في المراجع الحالية، خصوصًا حالتي Uploaded وError. أرسل Figma node الخاص بـFile Upload.

Avoid:

> أرسل مراجع أكثر.

---

# 23. Step 9 — Pre-Implementation Summary

Before significant code changes, provide a SHORT summary:

```text
Template:
[Name]

Sections:
- ...

Reuse:
- ...

Extend:
- ...

Create:
- ...

Files expected to change:
- ...
```

Then proceed automatically.

Do NOT wait for approval unless:

- There is a major architecture conflict
- References materially contradict each other
- A shared change may break existing templates
- The implementation is materially ambiguous

---

# 24. Step 10 — Build the Complete Template

Build the complete page.

Priority:

```text
Existing Components
        ↓
Existing Sections
        ↓
Safe Extensions
        ↓
New Reusable Components
        ↓
Template Composition
```

Always reuse:

- Header
- Footer
- Navigation
- Breadcrumb
- Shared page header
- Shared sections
- Existing layout conventions
- Existing utilities
- Existing tokens

Do not stop after creating individual components.

The final template should be complete and usable.

---

# 25. Visual Accuracy

When Figma exists, treat it as the primary visual reference.

Match where relevant:

- Widths
- Heights
- Container behavior
- Grid
- Spacing
- Padding
- Margins
- Typography
- Font weight
- Line height
- Borders
- Radius
- Icons
- Alignment
- Section spacing
- Component states
- Responsive behavior
- RTL behavior

Do NOT invent arbitrary values if equivalent project tokens already exist.

Prefer:

```text
Existing token
    ↓
Existing utility
    ↓
Existing component value
    ↓
New token only when truly required
```

---

# 26. CSS Rules

Do NOT:

- Duplicate existing CSS
- Add page-specific CSS when a shared component should own the styles
- Hardcode repeated design values unnecessarily
- Create separate RTL stylesheets
- Introduce framework-specific classes
- Add unrelated global styles

Prefer:

- Existing tokens
- Existing utility classes
- Component-scoped CSS
- Logical CSS properties
- Reusable variants

Template-specific CSS should remain minimal.

---

# 27. RTL Requirements

RTL support is mandatory.

Templates must work with:

```html
<html dir="rtl"></html>
```

and where applicable:

```html
<html dir="ltr"></html>
```

Prefer logical properties such as:

```css
margin-inline-start
margin-inline-end
padding-inline
border-inline-start
inset-inline-start
text-align: start
```

Avoid unnecessary directional duplication.

Do not create separate RTL markup implementations.

---

# 28. Responsive Requirements

Reuse the project's existing responsive architecture and breakpoints.

Do not create arbitrary breakpoints without justification.

Validate the relevant states, including when applicable:

- Desktop
- Tablet
- Mobile

Check:

- Navigation
- Grid
- Cards
- Typography
- Forms
- Tables
- Sidebars
- Images
- Section spacing
- Overflow
- Touch interactions

---

# 29. Accessibility Requirements

Accessibility is part of Definition of Done.

Use:

- Semantic HTML
- Correct heading hierarchy
- Keyboard accessibility
- Visible focus states
- Native interactive elements
- Appropriate labels
- Accessible forms
- Correct ARIA states where required
- Accessible accordions
- Accessible tabs
- Accessible modal behavior
- Adequate touch targets
- Reduced motion when relevant

Do not use ARIA when native semantic HTML already solves the problem.

Follow existing accessibility standards in the repository.

---

# 30. JavaScript Rules

Use Vanilla JavaScript only when behavior requires JavaScript.

Examples:

- Mobile navigation
- Accordion
- Tabs
- Modal
- Dropdown
- Interactive filters
- Search interactions

Rules:

- No inline JavaScript
- No framework dependencies
- Avoid global namespace pollution
- Prefer progressive enhancement
- Maintain keyboard accessibility
- Keep ARIA states synchronized
- Keep components independent where possible
- Do not use JS for styling that CSS can handle

---

# 31. Step 11 — Integration

Template construction and template integration are separate concerns.

After the template is complete:

Integrate it into the project where applicable.

Tasks may include:

- Add template to template index
- Add template to navigation
- Connect related templates
- Add relevant links
- Update template registry
- Ensure shared navigation remains consistent

Do NOT:

- Modify unrelated pages
- Refactor unrelated components
- Redesign global navigation
- Change unrelated routing

---

# 32. Shared Component Safety

If a shared component must change:

1. Identify current consumers.
2. Preserve backward compatibility whenever possible.
3. Make the smallest necessary change.
4. Use a reusable variant when appropriate.
5. Validate affected templates.
6. Avoid unrelated refactoring.

Never redesign an existing shared component solely to satisfy one template.

---

# 33. Repository Efficiency

Do NOT scan the entire repository without a reason.

Start with:

1. `docs/component-registry.md`
2. Target-template files
3. Shared components referenced by the target
4. Shared CSS / design tokens
5. Relevant sections
6. Template registry / navigation
7. Integration files

Inspect additional files only when necessary.

Do not repeatedly reread large files already understood unless they changed.

---

# 34. Context Efficiency

Minimize unnecessary context consumption.

Do NOT:

- Read unrelated directories
- Analyze unrelated templates
- Re-read large unchanged files
- Produce long internal reports
- Run broad repository searches without a purpose
- Repeat reference analysis
- Rediscover architecture already known

Prefer targeted inspection.

---

# 35. Testing During Development

Use focused tests during implementation.

Validate only what changed:

- New component
- Extended shared component
- Target section
- Target template
- Relevant responsive behavior
- Relevant accessibility behavior

Do NOT run the entire E2E/browser suite after every small change.

---

# 36. Final Validation

When the template is complete, validate:

- Template renders correctly
- Required sections exist
- Existing components were reused
- Extensions are justified
- New components are genuinely necessary
- No unnecessary duplicated HTML exists
- No unnecessary duplicated CSS exists
- No broken links exist
- Responsive behavior works
- RTL works
- Keyboard interaction works
- Accessibility remains valid
- Integration works
- Shared components remain functional

If a shared component was materially changed, perform the appropriate broader validation once at the end.

---

# 37. Component Registry Update

Before finishing, update:

```text
docs/component-registry.md
```

Add:

- Newly created reusable components
- New reusable sections if the registry tracks them
- New variants
- Relevant source locations
- Relevant implementation notes

Do not rewrite unchanged registry entries.

Keep the registry concise.

Its purpose is to:

- Reduce future repository scanning
- Prevent duplication
- Improve reuse
- Make future template work faster

---

# 38. Final Response

Keep the final response concise.

Use:

```text
Template:
[Name]

Reused:
- ...

Extended:
- ...

Created:
- ...

Integration:
- ...

Validation:
- ...

Issues:
- None
```

If there are unresolved issues, list only the important ones.

Do not provide a long narrative.

Do not explain unchanged code.

---

# 39. Mandatory Restrictions

Do NOT:

- Rebuild Header
- Rebuild Footer
- Duplicate navigation
- Duplicate shared CSS
- Introduce Bootstrap
- Introduce Tailwind
- Introduce React
- Introduce Next.js
- Introduce Drupal
- Replace the project's token system
- Change project naming conventions without necessity
- Perform unrelated refactoring
- Create a new component without checking existing ones
- Build page-specific components that should be reusable
- Add arbitrary visual values when project tokens exist
- Create separate RTL implementations unnecessarily
- Ignore existing standards or documentation
- Scan unrelated repository areas without reason

---

# 40. Golden Rules

1. Reuse before creating.
2. Inspect before implementing.
3. Understand the template before writing HTML.
4. Figma is the primary visual reference when available.
5. DGA defines government structure and UX context.
6. Live pages define real-world usage and behavior.
7. Existing project assets have implementation priority.
8. Components come before templates.
9. Sections should be reusable.
10. Variants are preferred over duplicated components.
11. Never duplicate Header or Footer.
12. Never duplicate CSS unnecessarily.
13. New components must be reusable.
14. Keep shared changes backward-compatible.
15. Ask for additional references only when required.
16. Ask for one specific missing reference at a time.
17. Continue from the same stage after receiving a reference.
18. Do not restart the entire workflow.
19. Build the complete template.
20. Integrate only after construction is complete.
21. Use focused testing during development.
22. Use broader validation only when justified.
23. Keep the component registry current.
24. Keep communication concise.
25. Every new template should make the next template easier to build.

---

# 41. Success Criterion

A successful implementation is not simply:

> The page visually matches the reference.

A successful implementation means:

- The page matches the approved references
- Existing architecture was preserved
- Reusable components were maximized
- Duplication was minimized
- New assets are reusable
- RTL works
- Responsive behavior works
- Accessibility is maintained
- The template integrates cleanly
- The design system becomes stronger after the template is added

The long-term objective is:

```text
Template 1
→ requires several reusable components

Template 2
→ reuses most of Template 1 infrastructure

Template 3
→ requires fewer new components

Template 10
→ is mostly composition of existing system assets
```

Every implementation decision should move the project toward that state.
