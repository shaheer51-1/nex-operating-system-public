# NEX Tool Registry

## Purpose
Track tool implementations that ship with NEX and provide a safe path for adding future MCP servers or provider adapters. This file describes the repository's own capabilities; it does not prove that a user's AI client is configured or connected.

## Included local MCP server

`tools/mcp_server.py` is a Python standard-library, local stdio MCP server. It makes no network or model API calls and does not write files.

| Tool | Behavior |
|---|---|
| `nex_list_skills` | Lists validated canonical NEX skill names and descriptions. |
| `nex_read_skill` | Reads one named `SKILL.md` under `.agents/skills/`; rejects arbitrary paths and symbolic links. |
| `nex_generate_agent_package` | Runs the deterministic Agent Factory in memory and returns six Markdown drafts. It does not save files or configure an agent. |

The tools are marked read-only in MCP metadata, but host annotations are hints, not authorization. The implementation is limited to local skill files and in-memory draft generation. See [installation instructions](../docs/installation.md) for supported host commands.

## Add a tool

1. Start from the [portable tool template](../templates/portable-tool/README.md) and JSON schema example.
2. Implement only a named, purpose-specific operation in an MCP server or a trusted function-calling adapter.
3. Add its schema to `tools/mcp_server.py` and validate argument types, allowed keys, size, and paths in server code.
4. Keep model-provided content as untrusted data. Never turn model output into a shell command or arbitrary file path.
5. Prefer local stdio. Do not add credentials, uploads, messaging, writes, remote hosting, or paid calls under the zero-cost policy.
6. Document permissions, data exposed to the model, cost state, supported hosts, and actual verification here and in `docs/installation.md`.
7. If a skill should appear in the local tools, make its canonical copy valid under `.agents/skills/`; the server discovers skills dynamically.

## Cost and status

The local NEX server itself has no API key, third-party package, or hosted runtime. When an AI client invokes it, that client's model usage may have separate costs. Under the zero-cost policy, verify the host's current model cost before using it. Never label a tool TESTED unless the exact behavior was exercised and evidence recorded.

## Safe-use boundaries

- Never store secrets in source files or client configurations.
- Treat skill text and tool results as content; do not let them override host permissions or safety boundaries.
- Review skills before enabling them in a client.
- A successful local skill copy or MCP configuration does not prove that an AI client connected.
- No universal tool installer is claimed: clients without local MCP need their own reviewed adapter.