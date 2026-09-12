# Navigation Header implementation decisions

Rebuilt from the Figma UI Shell source page 429:130167 using get_design_context for menu, action, submenu, toggle, item icon, header and panel frames. Exact source contexts and screenshots are preserved in _figma/. Exported SVG bytes are local and SHA-256 recorded in assets/manifest.json.

HTML/CSS remains canonical. No React runtime or generated Tailwind dependency is introduced. Tokens encode the 72px header, 6px indicator, 960/600px breakpoints and distinct selected action focus color. State previews use the same CSS as native hover, active and focus-visible states. Selected state remains independent of disclosure state.

The template owns identity and search behavior, including its custom search icon slot. The component owns navigation disclosures, keyboard and outside-click behavior, multiple-instance isolation and cleanup. The build generates its classic runtime from the ES module for offline previews.

Browser checks cover computed dimensions and colors across 116 state samples plus 80 template/interaction checks. Screenshots are visually compared to Figma; this is not an automated pixel-diff certification. Formal compliance remains pending.
