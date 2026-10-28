"""Local, read-only MCP tools for included NEX skills and agent drafts."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.agent_factory import render, validate  # noqa: E402

SUPPORTED_PROTOCOLS = ("2025-11-25", "2025-06-18", "2024-11-05")
MAX_LINE_BYTES = 2 * 1024 * 1024
MAX_SKILL_BYTES = 200_000
MAX_RESULT_CHARS = 100_000
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def skill_catalog() -> list[dict[str, str]]:
    base = ROOT / ".agents" / "skills"
    found = []
    if (ROOT / ".agents").is_symlink() or base.is_symlink() or not base.resolve().is_relative_to(ROOT.resolve()):
        return found
    if not base.is_dir():
        return found
    for folder in sorted(base.iterdir(), key=lambda item: item.name):
        if folder.is_symlink() or not folder.is_dir() or not NAME_RE.fullmatch(folder.name):
            continue
        skill_file = folder / "SKILL.md"
        if skill_file.is_symlink() or not skill_file.is_file() or skill_file.stat().st_size > MAX_SKILL_BYTES:
            continue
        text = skill_file.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            continue
        name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", parts[1])
        description = re.search(r"(?m)^description:\s*(.+?)\s*$", parts[1])
        if name and name.group(1) == folder.name and description:
            found.append({"name": folder.name, "description": description.group(1)})
    return found


def read_skill(name: object) -> str:
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        raise ValueError("Provide a valid lowercase skill name.")
    if name not in {entry["name"] for entry in skill_catalog()}:
        raise ValueError("Unknown NEX skill.")
    if (ROOT / ".agents").is_symlink() or (ROOT / ".agents" / "skills").is_symlink():
        raise ValueError("Skill directory is not a trusted local folder.")
    base = (ROOT / ".agents" / "skills").resolve(strict=True)
    if not base.is_relative_to(ROOT.resolve()):
        raise ValueError("Skill directory is outside the repository.")
    folder_path = ROOT / ".agents" / "skills" / name
    if folder_path.is_symlink():
        raise ValueError("Skill path is outside the approved directory.")
    folder = folder_path.resolve(strict=True)
    if not folder.is_relative_to(base):
        raise ValueError("Skill path is outside the approved directory.")
    file = folder / "SKILL.md"
    if file.is_symlink() or not file.is_file() or file.stat().st_size > MAX_SKILL_BYTES:
        raise ValueError("Skill file is unavailable or exceeds the read limit.")
    return file.read_text(encoding="utf-8")


AGENT_SCHEMA = {
    "type": "object",
    "properties": {
        "agent_name": {"type": "string"},
        "role": {"type": "string"},
        "goal": {"type": "string"},
        "project": {"type": "string"},
        "platform": {"type": "string"},
        "budget": {"type": "string"},
        "repository_url": {"type": "string"},
        "inputs": {"type": "array", "items": {"type": "string"}},
        "outputs": {"type": "array", "items": {"type": "string"}},
        "allowed_actions": {"type": "array", "items": {"type": "string"}},
        "prohibited_actions": {"type": "array", "items": {"type": "string"}},
        "acceptance_criteria": {"type": "array", "items": {"type": "string"}},
        "approval_triggers": {"type": "array", "items": {"type": "string"}},
        "data_boundaries": {"type": "array", "items": {"type": "string"}},
        "tools": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "capabilities": {"type": "string"},
                    "permission_scope": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["AVAILABLE", "CONNECTION-VERIFIED", "COST-VERIFIED", "TESTED", "UNVERIFIED", "BLOCKED"],
                    },
                    "cost_state": {"type": "string", "enum": ["FREE-VERIFIED", "PAID", "UNKNOWN"]},
                    "evidence": {"type": "string"},
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["agent_name", "role", "goal", "project"],
    "additionalProperties": False,
}


def tools_list() -> list[dict]:
    names = [entry["name"] for entry in skill_catalog()]
    return [
        {
            "name": "nex_list_skills",
            "description": "List included NEX skills. Reads local repository metadata only.",
            "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
            "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
        },
        {
            "name": "nex_read_skill",
            "description": "Read an included NEX skill by name. Reads only .agents/skills/<name>/SKILL.md.",
            "inputSchema": {
                "type": "object",
                "properties": {"name": {"type": "string", "enum": names}},
                "required": ["name"],
                "additionalProperties": False,
            },
            "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
        },
        {
            "name": "nex_generate_agent_package",
            "description": "Create six validated NEX agent Markdown drafts in memory. Does not write files, call a model, or access the network.",
            "inputSchema": AGENT_SCHEMA,
            "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
        },
    ]


def valid_agent_arguments(arguments: dict) -> bool:
    allowed = set(AGENT_SCHEMA["properties"])
    if set(arguments) - allowed:
        return False
    required = ("agent_name", "role", "goal", "project")
    if any(not isinstance(arguments.get(key), str) for key in required):
        return False
    string_fields = ("platform", "budget", "repository_url")
    if any(key in arguments and not isinstance(arguments[key], str) for key in string_fields):
        return False
    list_fields = (
        "inputs", "outputs", "allowed_actions", "prohibited_actions",
        "acceptance_criteria", "approval_triggers", "data_boundaries",
    )
    for key in list_fields:
        if key in arguments and (
            not isinstance(arguments[key], list)
            or any(not isinstance(item, str) for item in arguments[key])
        ):
            return False
    if "tools" in arguments:
        if not isinstance(arguments["tools"], list):
            return False
        tool_keys = {"name", "capabilities", "permission_scope", "status", "cost_state", "evidence"}
        for tool in arguments["tools"]:
            if not isinstance(tool, dict) or set(tool) - tool_keys:
                return False
            if not isinstance(tool.get("name"), str):
                return False
            if any(key in tool and not isinstance(tool[key], str) for key in tool_keys - {"name"}):
                return False
    return len(json.dumps(arguments, ensure_ascii=False).encode("utf-8")) <= 250_000

def call_tool(name: object, arguments: object) -> dict:
    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be an object.")
    if name == "nex_list_skills":
        return {
            "content": [{"type": "text", "text": json.dumps(skill_catalog(), ensure_ascii=False, indent=2)}],
            "isError": False,
        }
    if name == "nex_read_skill":
        return {"content": [{"type": "text", "text": read_skill(arguments.get("name"))}], "isError": False}
    if name == "nex_generate_agent_package":
        if not valid_agent_arguments(arguments) or validate(arguments):
            return {
                "content": [{
                    "type": "text",
                    "text": "Request validation failed. Complete required fields, remove placeholders and credentials, and use supported tool status and cost values.",
                }],
                "isError": True,
            }
        artifacts = render(arguments)
        output = "\n\n".join("--- " + filename + " ---\n" + text for filename, text in artifacts.items())
        if len(output) > MAX_RESULT_CHARS:
            raise ValueError("Generated output exceeds the safe response limit.")
        return {"content": [{"type": "text", "text": output}], "isError": False}
    raise ValueError("Unknown NEX tool.")


def rpc_response(request_id: object, result: object = None, error: dict | None = None) -> dict:
    message = {"jsonrpc": "2.0", "id": request_id}
    message["error" if error is not None else "result"] = error if error is not None else result
    return message


def handle(message: object) -> dict | None:
    if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"), str):
        return rpc_response(None, error={"code": -32600, "message": "Invalid JSON-RPC request."})
    if "id" not in message:
        return None
    request_id = message["id"]
    params = message.get("params", {})
    if not isinstance(params, dict):
        return rpc_response(request_id, error={"code": -32602, "message": "Invalid params."})
    method = message["method"]
    if method == "initialize":
        requested = params.get("protocolVersion")
        version = requested if requested in SUPPORTED_PROTOCOLS else SUPPORTED_PROTOCOLS[0]
        return rpc_response(request_id, {
            "protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "nex-local-tools", "version": "0.1.0"},
        })
    if method == "ping":
        return rpc_response(request_id, {})
    if method == "tools/list":
        return rpc_response(request_id, {"tools": tools_list()})
    if method == "tools/call":
        try:
            return rpc_response(request_id, call_tool(params.get("name"), params.get("arguments", {})))
        except (OSError, ValueError) as error:
            return rpc_response(request_id, {
                "content": [{"type": "text", "text": str(error)}],
                "isError": True,
            })
        except Exception as error:
            print("NEX MCP tool failed: " + type(error).__name__, file=sys.stderr)
            return rpc_response(request_id, {
                "content": [{"type": "text", "text": "The NEX tool failed safely. Check local server output."}],
                "isError": True,
            })
    return rpc_response(request_id, error={"code": -32601, "message": "Method not found."})


def main() -> int:
    while True:
        line = sys.stdin.buffer.readline(MAX_LINE_BYTES + 1)
        if not line:
            return 0
        if len(line) > MAX_LINE_BYTES:
            sys.stdin.buffer.readline()
            sys.stdout.write(json.dumps(rpc_response(None, error={"code": -32700, "message": "Message too large."})) + "\n")
            sys.stdout.flush()
            continue
        try:
            request = json.loads(line.decode("utf-8"))
            response = handle(request)
        except (UnicodeDecodeError, json.JSONDecodeError):
            response = rpc_response(None, error={"code": -32700, "message": "Parse error."})
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    raise SystemExit(main())

