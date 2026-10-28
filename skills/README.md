# NEX Skills and Guides

NEX distributes two portable Agent Skills. The canonical files live under `.agents/skills/`; Claude Code and Grok Build mirrors are kept alongside them. A file in this repository does not install or activate a skill in an AI client.

## Portable Agent Skills

| Name | Purpose | Host notes |
|---|---|---|
| [NEX Capability Author](../.agents/skills/nex-capability-author/SKILL.md) | Add and maintain portable skills, local MCP tools, and client adapters with clear permissions and cost boundaries. | Mirrored for Claude Code and Grok Build; install paths for four coding clients are documented. |
| [NEX QA Reviewer](../.agents/skills/nex-qa-reviewer/SKILL.md) | Review an approved change using read-only source access and evidence-based findings. | Requires the host to provide an approved repository reader; the skill itself grants no access. |

## Supporting guides

- [UI/UX review checklist](../docs/uiux-review-checklist.md): evidence-based review prompts; not an automated or standards-conformance audit.
- [Agent Builder guide](agent-builder.md): design notes for bounded assistant workflows.
- [Agency Agents adaptation](agency-agents-adaptation.md): selected review lenses adapted with upstream attribution in `THIRD_PARTY_NOTICES.md`.

See the [installation guide](../docs/installation.md) to install or export supported skills. Check each client’s current documentation before enabling a skill or configuring tools.
