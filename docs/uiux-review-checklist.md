# UI/UX Review Checklist

Use this checklist to review a screen or user flow. Tie every finding to evidence from the supplied design, implementation, or observed interaction. Mark unavailable evidence as **Not verified**; do not invent findings.

## Establish scope

- Identify the user goal, screen or flow, target client, viewport sizes, and available artifacts.
- Record which evidence is available: screenshots, live UI, interaction steps, source, accessibility tree, or research.
- State what cannot be assessed from the available evidence. A desktop screenshot alone cannot establish mobile behavior, keyboard support, or conversion outcomes.

## Review the experience

- **Task flow:** entry point, next action, completion, back/cancel paths, errors, recovery, and preserved input.
- **Visual hierarchy:** primary action, grouping, labels, reading order, spacing, and content density.
- **Responsive behavior:** narrow widths, zoom, reflow, touch target reachability, and overflow across relevant screens.
- **Accessibility:** semantic headings and controls, accessible names, keyboard operation, visible focus, contrast, error/status announcements, and reduced-motion behavior where applicable. Do not claim standards compliance without a suitable audit.
- **Content and feedback:** concise instructions, clear field labels, helpful validation, loading/success/failure states, and understandable consequences for destructive or paid actions.
- **Trust and conversion:** clear pricing and terms, no misleading urgency, no hidden costs, and no unsupported conversion claims.

## Report findings

For each finding, include:

- **Severity:** blocker, high, medium, or low, based on user impact and frequency.
- **Evidence:** exact screen, state, element, or source location observed.
- **Impact:** who is affected and what task becomes harder or impossible.
- **Recommendation:** a concrete, proportionate change.
- **Confidence and limits:** what was observed and what remains unverified.

Prioritize the smallest changes that address the strongest evidence. Separate verified defects from hypotheses and optional experiments.
