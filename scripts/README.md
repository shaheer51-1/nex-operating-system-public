# Local Scripts

The NEX utilities use Python's standard library and run on the user's computer. They make no model/API calls and require no third-party Python packages.

## List and install skills

From the repository root:

```powershell
py -3 scripts\install_capabilities.py list
py -3 scripts\install_capabilities.py install --client codex
```

Replace `codex` with `claude`, `grok`, or `cursor`. See [installation](../docs/installation.md) for client paths, project installs, MCP setup, export, and removal.

## Generate a draft package

Copy `examples/agent-factory-request.json`, fill it with non-sensitive example data, and review the input before running:

```powershell
py -3 scripts\agent_factory.py --input examples\agent-factory-request.json --output .\output\draft
```

The generator validates common credential fields as a heuristic safeguard, creates six Markdown drafts, and refuses to overwrite existing expected output files. The scan cannot guarantee that every secret will be detected. Never put credentials or private project content into the request.

## Run local verification

This distribution includes a local Windows verification script and a Python test suite:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_windows.ps1
```

The script runs the discovered tests, compiles Python modules, and smoke-tests the Agent Factory in a temporary directory. The check runs on your computer. This release copy includes no hosted Actions workflow. No test result is claimed by this document; report the result from the exact code you ran.

If PowerShell cannot find the script, open a terminal in the extracted repository folder and confirm that `scripts/verify_windows.ps1` exists before running it.
