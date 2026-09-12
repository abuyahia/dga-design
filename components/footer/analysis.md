# Footer implementation decisions

The eight source variants were read through Figma get_design_context. Source code and screenshots are retained in _figma/. Assets are exported bytes, with source URLs and SHA-256 manifests. The package uses HTML/CSS and composes the existing Link and Button components. A scoped token binding applies the footer instance's white-30% outlined border without replacing Button state behavior.

The layout uses logical properties, wrapping desktop columns and a two-column mobile layout below 600px. The mobile tools form a separate row and legal information is centered above the logos. Direction-specific spacing and the empty legal-caption slot present in the light LTR mobile source are preserved. Links wrap rather than clipping long content. Total heights are content-driven, never fixed to the reference screenshot size.

The canonical templates feed both the showcase generator and the government site build. Gallery links target a real local example destination. Reference arrow glyphs are not represented as social network logos. Site-specific identity and available destinations are supplied by the consumer; no fictitious social accounts or inert accessibility controls are added.

The package needs no JavaScript. Browser checks cover computed geometry, colors, fonts, assets, direction, breakpoint boundaries, native focus, and the optional navigation section. Reference heights are checked at the Figma desktop width and immediately below the mobile breakpoint. Screenshots are also reviewed visually. These checks are separate from formal standards certification.
