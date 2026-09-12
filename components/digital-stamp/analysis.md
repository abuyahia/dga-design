# Digital Stamp implementation decisions

The KKU homepage places its disclosure strip immediately before the main header. The local template follows that placement, retaining the visually hidden skip link as the first keyboard target and replacing its old utility strip.

Figma page 17274:104 was inspected through metadata after the canvas context call returned no selection. Design contexts for desktop/mobile and RTL/LTR open components include closed branches; the eight combinations are documented in reference.json. Six Arabic extension contexts were also read. Reference SVG exports are stored locally without redraws.

Native details/summary supplies disclosure semantics, Enter/Space activation and hidden-content focus handling without JavaScript. A small optional module adds Escape and cleanup. Registration is a real anchor only when explicit registry data is supplied; gallery registration values are identified as examples. The site remains in preview mode because it is a demonstration template, not a registered government site.

The implementation preserves Figma's direction-specific spacing and smaller mobile icons. The breakpoint is an implementation choice based on the existing 768px Base token because the source labels devices without a numeric threshold. Measured reference dimensions are verified at 1728px and 390px; intermediate widths wrap naturally. English extension copy beyond gov.sa is translated rather than asserted as verbatim Figma text.

Browser checks wait for the page lifecycle load event and local fonts before measuring or sending keyboard input. Formal compliance and actual government registration remain separate from implementation acceptance.
