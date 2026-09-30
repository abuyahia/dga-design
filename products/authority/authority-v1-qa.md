# Authority V1 QA — 2026-09-15

Status: **PASS**

## Coverage

- A03–A28 exit criteria passed.
- 35 generated HTML routes cover all 19 REQUIRED V1 page types.
- Demo records: 5 services, 4 news items, 4 programs/initiatives, 5 knowledge resources, and 3 regulatory documents.
- Default Home profile: `regulatory`; the same renderer was exercised with `enablement` and `development` policies.

## Final validation

- `python3 -B -m unittest discover -s tests -q`: 101 passed.
- `python3 scripts/audit.py --strict`: 0 errors, 0 warnings. The audit tool reports 309 inherited component rules as NOT RUN; used Authority surfaces are covered by the product browser gate below.
- Authority browser gate: 68/68 passed at 320, 768, and 1280 pixels in RTL and LTR, including keyboard navigation, filters, Service Tabs, no-JavaScript states, reduced motion, local styles/images, and horizontal overflow checks.
- `git diff --check`: passed.
- All 38 Authority JSON files parsed.
- Generated internal link/fragment/download graph: closed; no missing targets.
- Authority runtime references to `products/ministry/`: 0; Ministry assets in Authority output: 0.

## Regression builds

- Legacy/no argument: pass.
- `--config site/government.json`: pass.
- `--product ministry`: pass.
- `--product authority`: pass; output `dist/products/authority/`.

No REQUIRED V1 issue remains. Recommended and optional post-V1 capabilities remain deferred per `authority-v1-build-plan.md`.
