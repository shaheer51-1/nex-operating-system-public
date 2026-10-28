---
name: nex-capability-author
description: Create or update reusable NEX skills and tool packages from the portable templates. Use when adding a skill, MCP tool, provider adapter, or new AI client compatibility.
---

# NEX Capability Author

Use this skill to add reviewed, portable instructions and tool contracts to the NEX repository. A draft in Git does not install or activate it in an external client.

## Before editing

1. Read docs/portable-capabilities.md and the relevant template.
2. Inspect skills/README.md or tools/README.md for duplicates and naming conventions.
3. Identify the intended client surfaces. Separate model/chat product, coding client, API, and operating system.
4. Read current official documentation for any support or setup claims. Record the check date and link it.
5. Keep the operation within the NEX zero-cost policy. Unknown cost means BLOCKED; do not call provider APIs, publish a package, start a hosted runtime, install dependencies, or create a tunnel.

## Add a skill

1. Create a lowercase hyphenated directory under .agents/skills/.
2. Copy templates/portable-skill/SKILL.md and replace every placeholder.
3. Keep the core workflow client-neutral. Move platform-specific instructions to references/platforms.md.
4. Include when to use it, inputs, steps, expected result, safety/approval boundaries, evidence, and failure handling.
5. Add a row to skills/README.md with its purpose, compatible surfaces, and draft/verified status.
6. Keep `.agents/skills/<name>/SKILL.md` canonical. For Claude Code and Grok Build project support, add byte-for-byte copies under `.claude/skills/<name>/SKILL.md` and `.grok/skills/<name>/SKILL.md`; update all copies in the same change. Do not claim that a file is installed or activated just because it exists in Git.
7. Mark compatibility per client as Native, Adapted, Manual, or Unverified. Do not claim that a file is installed just because it exists in Git.
8. The local installer discovers valid skills from `.agents/skills/`; update `skills/README.md` and the Claude/Grok mirrors, but do not hard-code each skill name into the installer.
9. Do not copy a skill into a user profile or upload it unless the user requested that destination and current access/cost requirements are clear.

## Add a tool

1. Start from templates/portable-tool/tool-definition.json and README.md.
2. Define a single purpose-specific tool. Use the MCP name, description, and inputSchema contract where supported.
3. Implement the tool in a real server or trusted provider adapter. Do not make a generic shell-execution tool.
4. Validate all input, enforce authorization, minimize data, limit outputs, and report errors without leaking secrets.
5. Require explicit host approval for writes, deletion, publication, messaging, purchases, permission changes, or production operations.
6. For NEX's local tool server, add the implementation and strict schema validation to `tools/mcp_server.py`; keep stdout protocol-only and errors bounded.
7. Add the tool to tools/README.md with source, permissions, data handling, cost status, and verification status. Do not call it unless its current connection and cost are verified.

## Windows and other clients

- Keep the canonical skill in .agents/skills/<name>/. Codex and Cursor discover this project root; for other clients, document the exact project or user discovery path and keep any adapter copy/configuration synchronized with the canonical source.
- For Claude Code or ChatGPT plugin packaging, use their current documented skill locations/package format; keep any copy in sync with the canonical source.
- For local MCP, follow `docs/installation.md` and the selected client's current setup instructions. Keep values that contain secrets out of checked-in config; use environment variables or the app's secret store.
- For Qwen, identify the exact surface (Qwen-Agent, API, or chat app) before writing setup instructions.
- For DeepSeek API, document the client-side function-call adapter and validation loop. Do not claim native MCP or native SKILL.md loading without official evidence.
- Treat cloud skill sync, API calls, publishing, and remote tunnels as cost-unknown until checked.
- The portable skill ZIP and local installer do not configure client accounts. Host commands are user-run and should be reviewed first.

## Completion record

Report exact files and branch, compatibility evidence, what remains a draft, what was actually verified, and what was not run. Never infer activation or test success from a Git commit.
