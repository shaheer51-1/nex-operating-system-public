# NEX Agent Factory Workflow

Use this process to turn a plain-language agent request into a structured package. The local generator drafts files; it does not configure or execute agents.

## Step 1 — Intake
Copy and edit the JSON request at examples/agent-factory-request.json. Capture the goal, project, platform, budget, tool needs, data sensitivity, and success criteria. Do not include secrets.

## Step 2 — Inspect
Read the relevant project brief, [Tool Registry](../tools/README.md), current agent definitions, and platform documentation where available. Confirm repository identity before any write. Avoid duplicate roles.

## Step 3 — Normalize
Translate the request into one primary role, clear inputs, output contract, permitted actions, prohibited actions, and acceptance criteria. Mark missing values instead of inventing them.

## Step 4 — Resolve tools
For each tool, record exact capability, permission scope, connection state, cost evidence, and test status. Never infer that a listed tool is connected, free, or tested.

## Step 5 — Enforce budget and safety
Under zero-cost, no paid model/API calls, usage credits, metered automation, or recurring jobs. Unknown cost is a stop condition. The generator marks tools whose cost state is not FREE-VERIFIED as blocked for execution.

## Step 6 — Generate package
On Windows with Python available, run: py scripts/agent_factory.py --input examples/agent-factory-request.json --output output/qa-agent
The output contains agent-spec.md, system-instructions.md, tool-manifest.md, test-plan.md, setup.md, and checkpoint.md. The QA test plan includes evidence traceability, false-positive handling, untrusted repository instructions, read-only enforcement, test integrity, and report-write approval checks.

## Step 7 — Validate
The script validates required fields, rejects common placeholder text in required fields and a supplied repository URL, validates tool status/cost values, and scans for basic secret-like patterns. The secret scan is not a guarantee of secret detection. Review every generated file.

## Step 8 — Test
Run: py -m unittest tests.test_agent_factory -v
These tests have not been run by the connected GitHub tool session. Record results only after running them locally.

## Step 9 — Configure only with authorization
Configuration is a separate action. It requires a supported connected tool, verified permissions, known zero-cost execution, and any necessary user approval. Do not deploy, run, or schedule agents merely because a package was generated.

## Completion report
State files created, validation outcomes, tests actually run, assumptions, costs, blockers, and one next action.