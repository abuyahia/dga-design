# Page Intro composition

All compatible internal-page heading areas use `template.html` through
`scripts/page_intro_markup.py:render_page_intro`. Existing variants are unchanged.

The renderer retains its existing arguments and adds optional `breadcrumb_items`
(for the canonical variable-depth Breadcrumb renderer) and `description_markup`
(for trusted, already-escaped build fragments). Plain page title/eyebrow/description
and intro_extra text remain escaped. Missing optional text produces no empty wrapper.
`description-group.html` provides a lead plus supplementary paragraph when both
are present, as in Heavy Content; it is an existing-slot composition, not a variant.

Consumers: About, News, FAQ, Services, Form, Contact, Heavy Content and Service
Detail. Service Detail places only its breadcrumb/title in Page Intro: the launch
CTA remains an adjacent flex item, and tags, service description and agreement link
remain in the service overview. TOC, sidebars and forms stay outside Page Intro.
Home Hero and Error State retain their distinct page-purpose structures.

Shared presentation is owned by `sections/page-intro/page-intro.css`.
Contextual CSS may configure the scoped `--page-intro-*` properties for padding,
background, content padding/gap, title font/color/tracking and description
font/color/width. These are presentation inputs referencing existing tokens, not
new global scales or page-specific variants. The shared rules own actual heading,
description and gap declarations. Default values preserve existing consumers;
local rules retain flex/grid placement and original embedded geometry. No broader
stylesheet ownership migration is included.
