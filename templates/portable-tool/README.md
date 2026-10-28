# Portable MCP Tool Template

This folder is a starter contract for documenting a tool. It does not execute actions and is not a complete MCP server.

## Add a tool safely

1. Copy this folder into the implementation for the new tool and rename the definition file.
2. Replace the example name, description, and JSON Schema with one narrow operation.
3. Implement it in a real MCP server or a documented provider-specific function-call adapter.
4. Validate arguments in trusted code before touching files, services, or accounts.
5. Add authorization, rate limits, bounded outputs, safe errors, and an approval path for side effects.
6. Record permissions, data sent, cost status, test status, and failure modes in the NEX Tool Registry.
7. Use an actual client that supports the chosen protocol. A tool schema by itself is not a connection.

## Cross-client rules

- Prefer MCP when the client supports it.
- Preserve the JSON Schema input contract for adapters.
- For DeepSeek API, the trusted client converts the MCP definition into a function-call definition, checks arguments, calls only its named implementation, and returns the result.
- Treat annotations as hints; they do not grant permission or replace an approval.
- Never add a generic tool that executes arbitrary model-produced shell commands or code.
- Store credentials in the host application's secret store or environment; do not include values in files.

## Windows notes

Use the local transport/configuration documented by the specific Windows client. Prefer project-local configuration when available. Do not put secrets in a checked-in JSON file. Do not install packages, run a server, create a public endpoint, or tunnel local access under the zero-cost policy unless the exact operation is verified free and authorized.
