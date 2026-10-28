# Install NEX skills and local tools

NEX ships portable Agent Skills and a local MCP server. The installer uses Python's standard library, works on Windows, macOS, and Linux, and makes no network, model, API, or package-manager calls. It does not install an AI client, change account settings automatically, or make a hosted service.

See the [NEX privacy and data-handling notice](../PRIVACY.md) for what the local software does with data and what may be handled separately by your AI client or provider.

## Requirements

- Python 3.10 or newer.
- The AI client you want to use, installed separately.
- No API key, subscription, third-party Python package, or hosted runtime is required for the local NEX MCP tools.

## Get a local copy

Download and extract the repository ZIP, or clone it if you already have Git. Open a terminal in the repository folder.

Once public, anyone can download a copy, subject to the repository's license and the destination client's capabilities.

## Install skills

List the included skills:

    # Windows PowerShell
    py scripts\install_capabilities.py list

    # macOS/Linux
    python3 scripts/install_capabilities.py list

Install for one client at user scope:

    py scripts\install_capabilities.py install --client claude
    py scripts\install_capabilities.py install --client grok
    py scripts\install_capabilities.py install --client codex
    py scripts\install_capabilities.py install --client cursor

Install for all four supported coding clients:

    py scripts\install_capabilities.py install --client all

The script copies the canonical skills from .agents/skills into the client's documented user skill folder. Codex and Cursor use CODEX_HOME/skills and ~/.cursor/skills; Claude Code and Grok Build use ~/.claude/skills and ~/.grok/skills. On Windows, these are under your user profile. Project-scope installs use .agents/skills for Codex and Cursor, .claude/skills for Claude Code, and .grok/skills for Grok Build.

To install into an existing project folder instead of your user profile:

    py scripts\install_capabilities.py install --client claude --scope project --project-root C:\path\to\your-project
    py scripts\install_capabilities.py install --client all --scope project --project-root C:\path\to\your-project

Select one skill by repeating --skill for each requested name:

    py scripts\install_capabilities.py install --client claude --skill nex-qa-reviewer

The installer skips an identical copy. If a different skill already exists at the destination, it stops before changing anything. After reviewing that copy, --overwrite replaces it and preserves a timestamped backup.

To create an archive for manual import into another product that accepts Agent Skills:

    py scripts\install_capabilities.py export --output .\nex-skills.zip

The archive contains instructions and supporting files only. Import is product-specific. For ChatGPT chat, Claude web, Grok chat, Qwen chat, DeepSeek chat, or another product, use that product's own documented skill import feature if it has one. Do not assume that a local folder or ZIP installs into every chat product.

## Install NEX tools through MCP

The repository includes a local stdio MCP server at tools/mcp_server.py. It exposes three local tools:

- nex_list_skills lists the repository's canonical skills.
- nex_read_skill reads one named skill from .agents/skills only.
- nex_generate_agent_package returns six validated draft Markdown files in memory. It does not write files.

The server makes no network or model API calls, executes no shell commands from model arguments, and does not write files. The host AI application may still send prompts and tool results to its model provider or charge for model usage according to that provider's plan.

### Claude Code

From the NEX repository folder, add a user-scope local stdio server:

    claude mcp add --scope user --transport stdio nex -- py -3 C:\path\to\nex\tools\mcp_server.py

To keep the server scoped to this project, use --scope project instead. Claude Code may ask you to approve the project server.

### Grok Build

    grok mcp add nex -- py -3 C:\path\to\nex\tools\mcp_server.py

For a project-scoped server, add --scope project. Grok Build also reads the project skill files directly.

### Codex CLI

    codex mcp add nex -- py -3 C:\path\to\nex\tools\mcp_server.py

### Cursor

Add this server entry to the project's .cursor/mcp.json. Replace the example path with the absolute path to the checked-out repository:

    {
      "mcpServers": {
        "nex": {
          "command": "py",
          "args": ["-3", "C:\\path\\to\\nex\\tools\\mcp_server.py"]
        }
      }
    }

Restart or refresh the client and confirm that its MCP settings show the NEX server and tools. The setup commands update that client's configuration; review the command before running it. To remove the server later, use the client's documented removal command or remove the nex entry from its MCP configuration.

## Compatibility boundaries

| Product or host | Skills | NEX tools |
|---|---|---|
| Claude Code | Native project and user skill locations | Local MCP stdio |
| Grok Build | Native project and user skill locations | Local MCP stdio |
| Codex CLI | Native project skills under .agents/skills and user install | Local MCP stdio |
| Cursor | Native project skills under .agents/skills and user install | Local MCP stdio |
| ChatGPT web or Work | Use an account feature that accepts Agent Skills; no automatic account upload is included | Local stdio is for Codex CLI. ChatGPT app connectors may require a remote MCP server and account access; no remote hosting is included |
| Qwen | Qwen-Agent can be configured with skills as instructions; chat-product import varies | Use only a Qwen host that documents MCP support |
| DeepSeek | Supply instructions through a client feature that accepts them | The API's function-calling interface needs a trusted adapter; this repository does not provide one |
| Other LLMs | Import the ZIP or copy the SKILL.md only if the product documents support | Use a client that supports local MCP stdio, or build a reviewed provider adapter |

An LLM is not a single installation target: coding clients, chat products, APIs, and local agent frameworks use different skill and tool interfaces. NEX supports the documented paths above; it does not claim universal compatibility.

## Add future skills and tools

- Keep each canonical skill in .agents/skills/<name>/SKILL.md and update skills/README.md.
- Keep the Claude Code and Grok Build project mirrors byte-for-byte aligned with their canonical NEX skills.
- The installer discovers valid canonical skill folders automatically; no provider API is needed to publish a ZIP.
- Add a real implementation and input validation to tools/mcp_server.py for a new MCP tool, update tools/README.md and its schema, and document which client can use it.
- For a non-MCP provider, build a narrow adapter that validates tool arguments and invokes only named trusted implementations. Never execute model-generated shell commands.
- Review the destination product's current setup docs, permissions, and billing before connecting a new tool or using a model.

## Public-release note

The repository now includes an MIT license for NEX-owned material, a separate third-party notice, a copyright notice, and a privacy and data-handling notice. Before making the repository public, review the full Git history and all public-facing material for information intended to remain private, and review every included skill's redistribution terms. See the [public-release checklist](public-release-checklist.md).

## Official setup references

Recheck host documentation before installing because product paths and commands can change:

- Agent Skills: https://agentskills.io/specification
- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code MCP: https://code.claude.com/docs/en/mcp
- Grok Build skills and plugins: https://docs.x.ai/build/features/skills-plugins-marketplaces
- Grok Build MCP servers: https://docs.x.ai/build/features/mcp-servers
- Codex skills: https://developers.openai.com/codex/skills
- Codex MCP: https://developers.openai.com/codex/mcp
- Cursor skills: https://cursor.com/docs/skills
- Cursor MCP: https://cursor.com/docs/mcp
