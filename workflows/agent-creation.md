# NEX Agent-Creation Workflow

This workflow designs and, when authorized tools are available, configures a specialist agent. It is not an autonomous process.

## Stage 1 — Intake
Record the target problem, user, owning project, budget ceiling, platform, expected result, data sensitivity, and acceptance criteria.

## Stage 2 — Inspect
Check existing agent definitions and tool inventory. Verify the intended platform, current connection, permissions, schema, pricing/credits, and whether the desired action is supported. Avoid duplicate agents.

## Stage 3 — Design
Complete [Agent Spec](../templates/agent-spec.md). Define:
- One primary responsibility and explicit out-of-scope work.
- Allowed tools, least-privilege permissions, and data boundaries.
- Inputs, output contract, success criteria, and error handling.
- Human approval/escalation triggers.
- Cost ceiling, test plan, and disable/rollback procedure.

## Stage 4 — Cost and safety gate
Under zero-cost, proceed only when the exact action is verified to be free and does not consume paid credits. Do not retry an insufficient-credit failure. Do not schedule recurring/background work. Stop if the cost or data handling is unclear.

## Stage 5 — Configure
Use only the current connected platform tools and their documented schemas. Confirm the returned result. If only documentation can be created, mark the agent SPECIFIED, not CREATED or DEPLOYED.

## Stage 6 — Test
If a free, authorized run is available, test:
1. A normal in-scope request.
2. A request outside the agent's scope.
3. A request that attempts to reveal secrets or bypass permissions.
4. A tool failure or missing-input scenario.

Record exact outcomes. If execution is unavailable or not free, mark TEST NOT RUN / BLOCKED and do not claim the agent works.

## Stage 7 — Register and checkpoint
Record agent name, purpose, platform, allowed tools, verified status, cost evidence, test results, risks, owner, and disable procedure. Update the agent/tool register only with evidence-backed facts.

## Stop conditions
- Cost/credits unknown or nonzero under zero-cost.
- Tool connection missing or toolsConnected is false.
- Missing permission or unsupported operation.
- Secrets or sensitive data would be exposed.
- Actual state differs materially from the inspected state.
