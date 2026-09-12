# Progress Indicator — Component Contract

```
contract_version: 1.0.0
component_id: progress-indicator
status: stable
category: navigation
```

## Purpose

Shows a user's position in a short, ordered process. The desktop form presents the full vertical list; small screens present the current step and total in a compact radial summary.

## Structure and states

- Use a `nav` with a clear accessible label and an ordered list.
- Each `.progress-indicator__item` carries a one-based `data-progress-step`.
- Apply `.is-complete` to finished steps and `.is-current` plus `aria-current="step"` to exactly one current step.
- Keep step titles and descriptions concise. The order in the DOM is the process order in both RTL and LTR.
- The compact view repeats the current title and description because the full list is visually hidden on small screens.

## Behavior

The component is useful without JavaScript. A form assembly may update classes, `aria-current`, compact text, and its live status when navigation controls change the current step. It must not claim that form data was submitted.

## Responsive use

The parent controls placement. Use the vertical form in a side column on larger screens and place the compact form before the form content below 768px.
