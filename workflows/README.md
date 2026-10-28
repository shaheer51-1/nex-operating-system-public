# Standard Workflow

The full procedure, including acceptance evidence and stop conditions, is documented in [NEX Operating Workflow](../docs/operating-workflow.md).

## Quick sequence
1. **Intake** — outcome, project, constraints, budget, scope, acceptance criteria.
2. **Inspect** — repository state, existing files, dependencies, behavior, and tests.
3. **Plan** — smallest sequential milestone, validation, risks, and rollback.
4. **Execute** — scoped changes only; stop on unexpected state or unclear cost.
5. **Verify** — label each check PASS, FAIL, NOT RUN, BLOCKED, or NOT APPLICABLE.
6. **Review** — relevant correctness, security, privacy, accessibility, and performance risks.
7. **Checkpoint** — record changes, evidence, limitations, blockers, and one next action.

## Specialized workflows
- [Agent Creation](agent-creation.md) — define, configure, safely test, and register agents only when platform access and cost permit.
- [Agent Factory](agent-factory.md) — convert a plain-language request into a structured, validated agent package draft without paid model execution.
- [Agency Agents Adaptation](../skills/agency-agents-adaptation.md) — apply curated code-review, evidence-QA, application-security, and UI finish-gate lenses where relevant.

A milestone is VERIFIED only when all required acceptance criteria have supporting evidence. A commit alone does not prove application behavior.
