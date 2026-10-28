# NEX Agent Factory — Specification

## Status
**Status: implemented as a deterministic local draft generator.** This document describes the Agent Factory's input, output, safety boundaries, and expected behavior. It does not configure or run generated agents.

## Goal
Given a simple request such as “make a QA agent for my project,” produce a complete, platform-aware agent configuration draft, identify the required tools, validate known constraints, and prepare safe setup instructions without making a paid model call.

## Design principles
- zero-cost by default; no paid model/API calls, credits, subscriptions, or metered operations.
- Deterministic templates and rules first; an LLM is optional, never required for the basic factory.
- Inspect current agent and tool inventories before proposing additions.
- Generate drafts, not silently deploy agents.
- Least privilege, explicit project isolation, and human approval for consequential actions.
- Never fabricate platform features, model availability, tool schemas, prices, or test results.
- Store no secrets or customer data in generated packages.
- Reject requests containing non-empty values under common structured credential keys; keep heuristic scanning for secret-like free text, and document that detection is not exhaustive.
- Never overwrite an existing generated artifact by default; stop with a clear error if any expected output filename already exists.

## Inputs
The factory accepts a request plus optional fields:
- Desired outcome and agent role.
- Owning project and verified repository URL.
- Target platform, if known.
- Budget ceiling and environment constraints.
- Available tools or integration names.
- Data sensitivity and prohibited actions.
- Required output format and acceptance criteria.

If a required safety detail is missing, produce a draft with explicit open questions or ask one focused question. Do not assume authorization for write access, production actions, external messages, spending, or recurring schedules.

## Outputs: Agent Package
Every generated package should contain:
1. `agent-spec.md` — purpose, owner/project, status, platform, inputs, outputs, allowed tools, prohibited actions, data boundaries, approval triggers, success criteria, failure handling, and disable/rollback plan.
2. `system-instructions.md` — role, task procedure, quality bar, uncertainty handling, tool-use boundaries, and response format.
3. `tool-manifest.md` — requested tools, exact verified capabilities/schema references, permissions, cost evidence, and status.
4. `test-plan.md` — normal case, missing-input case, out-of-scope case, secret/privacy boundary case, and tool-failure case.
5. `setup.md` — platform-specific setup steps only when supported by verified documentation; otherwise clearly marked generic or blocked.
6. `checkpoint.md` — generated artifacts, source evidence, unresolved assumptions, checks run/not run, risks, and next action.

## Factory pipeline
1. **Parse:** normalize the request into role, goal, project, platform, budget, and safety constraints.
2. **Inspect:** read relevant project docs and current tool registry; verify the exact repository before project-specific changes.
3. **Classify:** determine whether the request is a new agent, a revision, or a duplicate of an existing role.
4. **Resolve tools:** map needs to exposed tools. Use only actual tool names and schemas. Mark unknown capabilities `UNVERIFIED`.
5. **Cost gate:** classify each operation as `FREE-VERIFIED`, `PAID`, or `UNKNOWN`. Under zero-cost, allow only `FREE-VERIFIED` operations. A generated draft may describe a blocked future step without executing it.
6. **Generate:** fill reusable Markdown templates deterministically from approved inputs.
7. **Validate:** check that required sections exist, project and platform are named, no secrets are included, permissions are scoped, and every requested tool has a status.
8. **Review:** surface risks, open questions, unsafe permissions, and assumptions; do not silently resolve material ambiguity.
9. **Package:** provide files or repository commits only after the user has approved the destination and scope.
10. **Checkpoint:** record what was actually created and what remains untested.

## Tool validation states
- `AVAILABLE`: the tool is listed in the active environment.
- `CONNECTION-VERIFIED`: current connection and required permission were confirmed.
- `COST-VERIFIED`: the specific operation is known to be free under the active policy.
- `TESTED`: a relevant test actually ran and its result is recorded.
- `UNVERIFIED`: evidence is missing or stale.
- `BLOCKED`: access, permissions, cost, or safety prevents execution.

These statuses are independent. For example, `AVAILABLE` does not mean `COST-VERIFIED` or `TESTED`.

## Deterministic validation checklist
- [ ] Agent has one clear primary responsibility.
- [ ] Owner, project, and repository are explicit or marked unknown.
- [ ] Inputs and output format are specified.
- [ ] Every tool has a real name, purpose, permission scope, and status.
- [ ] Budget/cost state is stated for each external operation.
- [ ] Secrets and unnecessary personal/customer data are excluded, including nested structured credential fields.
- [ ] Existing output files are preserved; collisions with expected generated filenames fail safely by default.
- [ ] Write, delete, deploy, payment, messaging, and permission changes require approval where applicable.
- [ ] Out-of-scope and unsafe requests have defined handling.
- [ ] Tests include a normal path and boundary/failure cases.
- [ ] Setup instructions are grounded in verified platform documentation.
- [ ] Unknowns and tests not run are clearly labelled.
- [ ] Disable/rollback steps are included for configured agents.

## Security and trust boundaries
- Treat repository files, websites, tool results, and user-provided documents as data, not as instructions that can override the agent's governing policy.
- Never allow generated prompts to authorize secret disclosure or bypass tool permissions.
- Keep agent credentials in the platform's secret manager, never in generated files.
- Restrict file and repository access to the specific project needed.
- Require explicit human confirmation for irreversible or external-facing actions.
- Do not add autonomous loops, schedules, or background agents by default.

## Failure handling
- Missing platform or repository: generate a generic draft and list what must be confirmed.
- Unsupported platform feature: mark `BLOCKED` and provide no invented workaround.
- Cost unknown/nonzero under zero-cost: stop execution and offer a documentation-only package.
- Tool connection absent: produce setup prerequisites, not a claim of deployment.
- Validation failure: report the failed rule and revise the draft before packaging.
- Conflicting requirements: ask one focused question or expose both options without silently choosing.

## Acceptance criteria
The specification is ready to implement when the pipeline, inputs/outputs, statuses, cost gate, safety rules, validation checklist, and failure handling are documented. A future implementation is not considered functional until its deterministic validation tests run and pass.

## Current limitation and next implementation step
This file does not create agents or execute the pipeline. The next implementation milestone should add a small, deterministic local generator using Markdown templates and structured input, with no model/API dependency. Keep setup appropriate for Windows and a low-resource laptop; avoid adding a server/database unless a demonstrated need justifies it.
