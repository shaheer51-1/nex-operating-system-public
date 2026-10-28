# Portable Skills and Tools

**Purpose:** Give NEX and its user a repeatable way to add skills and tools that can travel across assistant products where their capabilities allow it.

This is a shared-format workflow with a local installer for supported coding clients, not a universal installer. Skill instructions and tool interfaces are different things: a skill teaches an assistant how to do a repeatable job; a tool gives it a controlled way to read or change an external system. Use the [NEX installation guide](installation.md) for copy, export, and local MCP setup.

## The shared formats

### Skills: Agent Skills

Author the reusable procedure as a folder containing a SKILL.md file with YAML frontmatter for name and description. Keep supporting references, scripts, and assets beside it. See the [Agent Skills specification](https://agentskills.io/specification).

NEX's canonical project location is:

    .agents/skills/<skill-name>/SKILL.md

Codex and Cursor discover project skills in this location. Claude Code discovers project skills in `.claude/skills/<skill-name>/SKILL.md`, and Grok Build discovers project skills in `.grok/skills/<skill-name>/SKILL.md`. NEX keeps `.agents/skills/` canonical and commits byte-for-byte copies of supported skills under both host-specific roots. Update every copy in the same change whenever its canonical source changes. These project files make skills discoverable to each host; they do not install the host or activate an agent. The no-network `scripts/install_capabilities.py` can also copy canonical skills to the user-level folders supported by Claude Code, Grok Build, Codex CLI, and Cursor, or export a ZIP for manual import. It never edits client settings.

### Tools: MCP and JSON Schema

The included local server at `tools/mcp_server.py` exposes NEX skill listing/reading and deterministic agent-package drafting over local stdio MCP. It has no third-party dependencies, does not write files, and makes no network/model calls. For new tools, when a client supports the Model Context Protocol (MCP), use an MCP server as the tool interface. Each tool has a unique name, description, and JSON Schema inputSchema. A tool definition does not implement the action; the server must validate arguments, enforce authorization, perform the action, and return a result. MCP annotations are descriptive hints and are not permission controls. See the [MCP tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools).

For clients that expose function calling instead of MCP, adapt the same JSON Schema and implement a trusted application-side loop. Validate model-produced arguments before execution. Never build a generic runner that blindly turns model output into shell commands.

## Compatibility levels

- **Native:** official documentation describes the package format or protocol in that client.
- **Adapted:** use a documented bridge or application-side adapter.
- **Manual:** provide the instructions as context; no native skill loader is claimed.
- **Unverified:** current official support could not be confirmed.

Compatibility is separate from cost, plan access, and permission. A native tool call is not automatically free, and having a schema is not authorization to execute it.

## Platform matrix

| Target | Skills | Tools | Practical note |
|---|---|---|---|
| ChatGPT and Codex | Agent Skills are the shared instruction format. Codex discovers project skills under .agents/skills. ChatGPT plugin packaging uses a skills/ directory; API-hosted skill attachment is a separate API feature. | MCP is the preferred shared contract. ChatGPT custom MCP app availability is plan/workspace dependent; Codex plugins can package MCP configuration. | Do not assume a repository folder automatically installs a ChatGPT skill. Do not upload a skill or call an API under zero-cost without checking current account cost and plan access. |
| Claude Code | Native Agent Skills support; project `.claude/skills/` and user-level installation through the NEX installer. | Local stdio MCP is supported; NEX includes a read-only local server. | Review skills before enabling. Client settings are changed only by the host command the user runs. |
| Grok Build | Native project-skill support through `.grok/skills/<skill-name>/SKILL.md`; NEX installer supports its user folder too. | Local stdio MCP; NEX includes a read-only local server. | Grok Build is distinct from Grok Bot. Grok Bot has a separate in-app skill library; do not treat it as a Windows-local install or as zero-cost. |
| Cursor | Native Agent Skills support in `.agents/skills/`; NEX installer supports its user folder. | Local MCP servers can be configured in `.cursor/mcp.json`. | Cloud skill sync is a separate account feature and may upload files; the installer does not enable it. |
| Qwen | No general SKILL.md loader for the Qwen chat product is claimed here. In Qwen-Agent, provide the workflow as instructions/context for the application. | Qwen-Agent documents MCP configuration; Qwen models also support function/tool calling through supported hosts. | State which Qwen surface is in use (Qwen-Agent, API, or chat product). Each host may use a different tool-call format. |
| DeepSeek | No native SKILL.md loader is claimed here. Supply the relevant instructions through the application/client context. | DeepSeek API documents function calling with JSON Schema. Use an application-side adapter to translate MCP tools into function definitions and dispatch calls safely. | The client must validate arguments and execute approved operations. API use may be metered; treat cost as UNKNOWN until checked. |
| Windows | Host operating system, not a model client. The Python installer and skill packages are cross-platform. | The bundled local MCP server uses Python's standard library and stdio. | The installer makes no network calls and never edits application settings. Follow each host's documented configuration steps; do not expose a server through a tunnel under zero-cost. |

Official sources checked 2026-10-28: [OpenAI skills](https://developers.openai.com/plugins/concepts/skills), [OpenAI API skills](https://developers.openai.com/api/docs/guides/tools-skills), [OpenAI MCP](https://developers.openai.com/api/docs/guides/tools-connectors-mcp), [Claude Code skills](https://code.claude.com/docs/en/skills), [Grok Build skills and plugins](https://docs.x.ai/build/features/skills-plugins-marketplaces), [Grok remote MCP](https://docs.x.ai/developers/tools/remote-mcp), [Grok Bot skills](https://docs.x.ai/grok-bot/skills-routines-and-automations), [Cursor skills](https://cursor.com/docs/skills), [Cursor MCP](https://docs.cursor.com/context/model-context-protocol), [Qwen-Agent](https://qwen.readthedocs.io/en/v3.0/framework/qwen_agent.html), [DeepSeek tool calls](https://api-docs.deepseek.com/guides/tool_calls/).

## Add a skill

1. Start with the template at templates/portable-skill/SKILL.md.
2. Choose a lowercase hyphenated name and make it match the folder name.
3. Write a short description that says what the skill does and when to use it.
4. Keep instructions provider-neutral. Put client-specific setup in a references file or in this guide, not in the core procedure.
5. Separate information gathering from actions that write, delete, publish, spend money, change permissions, or contact people.
6. State input requirements, expected output, failure handling, evidence, and any approval gate.
7. Save the canonical copy under `.agents/skills/<skill-name>/` and add it to `skills/README.md`.
8. For Claude Code and Grok Build project support, copy the same `SKILL.md` into `.claude/skills/<skill-name>/` and `.grok/skills/<skill-name>/` respectively. Keep every mirror byte-for-byte synchronized with the canonical file; do not claim installation or activation.
9. The installer and local MCP server discover canonical skills automatically. Update `skills/README.md` and the host mirrors; do not add a provider API call.
10. Mark each client Native, Adapted, Manual, or Unverified. Record exact installation steps in `docs/installation.md` only when officially documented.

For Claude Code, ChatGPT plugin packaging, or another client with a different root, use that client's documented directory or package format. Do not promise that one file path is discovered everywhere.

## Add a tool

1. Start with templates/portable-tool/README.md and tool-definition.json.
2. Define one narrow action with a unique name, plain description, and precise input schema.
3. Implement the action in `tools/mcp_server.py` or an explicit provider adapter. The portable JSON template alone is not runnable. Add an input schema and strict server-side validation; do not rely on the model or host to validate.
4. Validate every argument in trusted code; enforce access controls and rate limits; bound and sanitize results.
5. Mark whether the tool reads or changes data, what data it receives, what approval is required, and what cost evidence exists in tools/README.md.
6. Keep secrets in the selected client's secret store or environment, never in the repository, config examples, tool output, or skill instructions.
7. Prefer local stdio for Windows and other desktop setups when the client supports it. Document exact host setup and removal steps in `docs/installation.md`. Do not expose the server publicly or use a tunnel under zero-cost without verifying current cost and security.

For DeepSeek, a trusted client must convert the shared JSON Schema into the provider's function-call format, validate the returned arguments, execute only the named implementation, and return the result. Do not let the model choose arbitrary code or shell commands.

## Add another client later

Add a platform row only after checking that vendor's official docs. Record separate skill and tool support, exact install/discovery path, API or plan requirements, Windows notes, and cost state. If official evidence is missing, mark Unverified. Recheck this guide before using it for a live setup because product support can change.

## NEX zero-cost boundary

The local workflow does not require API calls, hosted runtimes, model tokens, remote tunnels, cloud agents, or skill publishing. Those operations may consume money or credits; verify their current cost and obtain the user's approval before using them. If cost is unclear, leave the operation at documented guidance and do not execute it.
