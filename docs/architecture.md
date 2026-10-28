# NEX Architecture

## Purpose

NEX packages reusable assistant instructions and a small set of local tools for coding workflows. It runs on the user's computer and has no NEX-hosted runtime.

## Components

1. **Portable skills:** canonical Agent Skills live in `.agents/skills/`. Claude Code and Grok Build mirrors are kept in their documented project-level folders.
2. **Installer and exporter:** `scripts/install_capabilities.py` lists, copies, and exports skill files. It does not configure client accounts or call an API.
3. **Local MCP server:** `tools/mcp_server.py` exposes skill listing, skill reading, and in-memory draft generation over local stdio.
4. **Agent Factory:** a deterministic Python utility reads a local JSON request and drafts six Markdown files. It does not call a model, connect tools, configure an agent, or run generated instructions.
5. **Reference material:** setup guidance, a UI/UX review checklist, templates, and a small local verification suite.

## Data flow

- A user chooses a client and installation scope; the installer copies canonical skill files to that local destination.
- A compatible client launches the MCP server as a local subprocess. The server reads only named NEX skill files or drafts package text in memory.
- Agent Factory reads a user-selected JSON file and writes draft files only to a user-selected local folder.

NEX utilities make no model/API calls or telemetry requests. A connected AI client may independently transmit prompts, repository content, or tool results to its provider under that provider's terms and billing.

## Boundaries

- A skill is guidance; it does not grant permissions or install itself in a client.
- MCP tool annotations are descriptive and do not replace host authorization.
- The local server does not run shell commands or write files.
- Generated agent documents are drafts, not deployed or autonomous agents.
- Client paths and capabilities vary. See the [installation guide](installation.md) and the [portable capabilities guide](portable-capabilities.md).

## Design choice

Keep the local utilities dependency-light and auditable. Add a hosted service, provider adapter, or external integration only when it provides clear value and its permissions, data handling, and cost are documented.
