# NEX — Portable AI Skills and Local Tools

Install reusable AI assistant skills across coding clients and run a small local MCP server for reading skills and drafting agent documents. NEX is a local-first toolkit, not a hosted autonomous agent.

## Get started

Requires Python 3.10 or newer. From a local copy of this repository:

```powershell
py -3 scripts\install_capabilities.py list
py -3 scripts\install_capabilities.py install --client codex
```

Replace `codex` with `claude`, `grok`, or `cursor`. See the [installation guide](docs/installation.md) for Windows, macOS, Linux, project-level installs, MCP setup, and manual skill export.

## What’s included

- **Portable skills:** `nex-capability-author` helps contributors add skills and tools; `nex-qa-reviewer` provides read-only, evidence-based change reviews.
- **[UI/UX review checklist](docs/uiux-review-checklist.md):** a repeatable checklist for usability, responsive behavior, accessibility, and evidence-based recommendations. It is guidance, not an automated accessibility or conversion audit.
- **Local MCP tools:** `nex_list_skills`, `nex_read_skill`, and `nex_generate_agent_package` list/read skills and draft agent-package text locally.
- **Agent Factory:** generates six draft Markdown files from a local JSON request. It does not call a model, configure an agent, or run generated instructions.
- **Extensible templates:** add skills and MCP tool contracts using the [portable capabilities guide](docs/portable-capabilities.md).

## Client support

| Client or platform | Current path |
|---|---|
| Claude Code, Grok Build, Codex CLI, Cursor | Installer-supported skill folders; local MCP setup is documented |
| ChatGPT, Qwen, DeepSeek, other AI products | Manual skill export or product-specific setup where supported; no universal installer or adapter is included |
| Windows, macOS, Linux | Python installer and local utilities; see the installation guide |

Compatibility is specific to each client and version. NEX does not claim every feature works in every AI product.

## Local operation and privacy

The installer and local MCP server make no network or model API calls. The Agent Factory works with local files. NEX does not operate a hosted runtime or send usage telemetry. Your AI client may separately send prompts, repository content, and tool results to its provider and may incur provider charges. Read [PRIVACY.md](PRIVACY.md) before using NEX with private repositories or sensitive content.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) to suggest a skill, tool, or documentation improvement. Report vulnerabilities using the private reporting route in [SECURITY.md](SECURITY.md).

## License and notices

NEX-owned material is licensed under MIT. See [LICENSE](LICENSE), [COPYRIGHT.md](COPYRIGHT.md), and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

