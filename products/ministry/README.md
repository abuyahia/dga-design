# Ministry Product Boundary

`product.json` is the Ministry product entry point. The product build reuses the
canonical Foundation source and currently adapts `site/government.json` only for
concerns that have not moved to product inputs. `navigation.json`, `footer.json`
and `pages/index.json` are owned by the product.

Build the product with:

```sh
python3 scripts/build_site.py --product ministry
```

The default output is `dist/products/ministry/`.

`pages/index.json` is the authoritative page registry. Its v1 shape is:

```json
{
  "schema_version": 1,
  "pages": ["example.json"]
}
```

Each registry value is a JSON definition inside `pages/` with this exact shape:

```json
{
  "id": "example",
  "route": "example.html",
  "renderer": "page-intro",
  "content": "example.json"
}
```

M01 introduced the registry empty. M02–M04 register `about.json`,
`strategy.json`, and `minister.json` with fictitious records in `content/demo/`.
Page and content references must remain inside their respective product
directories and must resolve to existing JSON objects. Content references are
relative to `content/demo/`. Renderer IDs are allow-listed by the builder and
determine the executable section composition; page data cannot supply template
paths or override renderer fields. A registered route replaces the same
transitional route while all other `source_config` pages remain available.

The registered shared renderer IDs at M01 are `page-intro`, `heavy-content`,
`contact`, `faq`, `form-template`, `error-state` and `service-catalog`. Later
packages may add an ID only when their shared or Ministry-owned renderer exists;
registry data never supplies an executable path.

`minister-profile` is a Ministry-only renderer. Its fixed registration resolves
`templates/minister-profile/renderer.py`, validates the V1 record contract, and
loads its scoped CSS. The portrait placeholder is a product asset with source
metadata under `assets/minister-profile/`.

`content/demo/` owns fictitious preview content, `templates/` owns Ministry-only
templates, and `assets/` owns Ministry-only assets. About and Strategy reuse the
shared Heavy Content renderer and therefore have no product templates. Minister
Profile is product-owned and composes canonical Page Intro, Breadcrumb, Avatar,
List, Link, and Feedback assets. A separate content index is unnecessary because
the page registry contains validated direct references. Shared components,
sections, partials, templates, styles and scripts remain at the repository root
and must not be copied here.
