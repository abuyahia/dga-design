# Minister Profile V1 Contract

This is a Ministry-owned page capability selected only by the registered
`minister-profile` renderer ID.

## Required fields

| Field | Contract |
|---|---|
| `title` | Nonempty Page Intro and document title |
| `description` | Nonempty Page Intro summary |
| `name` | Nonempty fictitious Minister name |
| `official_title` | Nonempty fictitious official title |
| `portrait` | Existing `.svg`, `.png`, `.jpg`, `.jpeg`, or `.webp` path contained by `products/ministry/assets/` |
| `portrait_alt` | Nonempty meaningful alternative text |
| `biography` | Nonempty plain-text biography |
| `updated` | Valid ISO `YYYY-MM-DD` date |

## Optional fields

- `message`: nonempty plain text when present.
- `appointment_date`: valid ISO `YYYY-MM-DD` date when present.
- `qualifications` and `experience`: nonempty lists of nonempty plain text.
- `role_information`: nonempty plain text describing the Minister's leadership
  relationship to the fictitious Ministry.
- `related_links`: nonempty `{label, href}` records using safe flat internal
  routes or HTTPS destinations without embedded credentials.

Optional fields render no heading, wrapper, or placeholder when omitted. All
record text and attributes are escaped. Page configuration cannot select a file
path; the shared builder maps the allow-listed renderer ID to this fixed product
module and template.

## Content and accessibility hierarchy

The Page Intro provides the single H1, `معالي الوزير`, and a lead sourced from
`description`. The identity block exposes the portrait, name, and official title.
Optional sections follow in this order: message, biography, qualifications,
professional experience, appointment/leadership information, then related
institutional links. The portrait always requires meaningful alt text, section
headings remain H2, and dates use semantic `time` markup.

The shared shell produces the title pattern `معالي الوزير | {site_name}` and the
meta description from `description`. Person structured data is intentionally
omitted because the demo record is fictitious and must not imply a real official
identity.
