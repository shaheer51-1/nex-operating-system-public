# Contributing to NEX

Thanks for helping improve portable AI skills and local tools. Small, clear contributions are easiest to review.

## Before opening a pull request

- Explain the user problem and the behavior you want to change.
- Keep changes narrow and update the relevant docs.
- Never include secrets, private repository content, personal data, or credentials in examples, issues, commits, or tests.
- Keep skills provider-neutral where practical. Keep canonical skills under `.agents/skills/<name>/`; update client mirrors where required.
- For new tools, document inputs, permissions, local data access, network behavior, supported clients, and cost state. Do not execute model-generated shell commands.
- Do not add a hosted service, telemetry, paid API, or provider dependency without a separate design and explicit approval.

## Local verification

The repository includes a Windows verification script that runs the unit tests, compiles the Python scripts, and smoke-tests Agent Factory output in a temporary folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_windows.ps1
```

This runs locally; it does not trigger GitHub Actions. Hosted workflow use may consume an account allowance or incur charges. Do not assume it is free.

## Pull request checklist

- [ ] Describe the change and its user-facing impact.
- [ ] Update documentation and compatibility notes.
- [ ] Run relevant local verification and report the exact result, or state that it was not run.
- [ ] Confirm no private data, credentials, or unrelated generated files are included.
- [ ] Note any change to permissions, network access, dependencies, or cost.
