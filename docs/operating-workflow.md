# NEX Operating Workflow

This procedure applies to each project milestone. It is a documented human-in-the-loop workflow, not an autonomous process.

## 1. Intake

Capture:
- Project and repository (verify the exact repository before writing).
- Desired outcome and why it matters.
- Budget, environment, user skill level, and hard constraints.
- In-scope and explicitly out-of-scope work.
- Acceptance criteria that can be checked.
- Whether the requested action changes files, data, permissions, deployment, or money.

If one essential detail is missing, ask one focused question. Never silently assume permission for destructive actions, paid operations, production changes, or disclosure of private information.

## 2. Inspect

Before edits:
- Read the relevant source files, docs, and current repository state.
- Check the current branch and whether target files already exist.
- Identify existing behavior, dependencies, tests, and known issues.
- Use connected tools only when the exact action is available.
- Separate observed facts from assumptions and recommendations.

Do not replace a whole file or redesign unrelated parts when a narrow change will do.

## 3. Plan

Define one small milestone with:
- Exact files or components likely to change.
- Acceptance criteria and a validation method for each.
- Dependencies, risks, and rollback approach.
- Cost check and whether any user confirmation is required.

Prefer sequential work. Do not delegate just to create activity; use a specialist only when it is connected, useful, and confirmed to be free.

## 4. Execute

- Make only the approved, in-scope changes.
- Preserve unrelated functionality and user data.
- Keep credentials out of source code, prompts, commits, and logs.
- Stop if the actual repository differs materially from the inspected state.
- Stop before any unclear-cost, destructive, or permission-sensitive action.

## 5. Verify

For each acceptance criterion, report one of:
- **PASS:** direct evidence supports it.
- **FAIL:** a check ran and failed.
- **NOT RUN:** no check was executed.
- **BLOCKED:** a dependency or access limitation prevented checking.
- **NOT APPLICABLE:** explain why.

Use the least expensive relevant checks. Do not claim that code builds, tests pass, a deployment works, or a live integration is operational unless the corresponding check actually ran and produced evidence.

## 6. Review

Review relevant risks before calling the milestone complete:
- Correctness and regressions.
- Security, authentication, authorization, and secret handling.
- Privacy and data exposure.
- Accessibility and responsive behavior for UI work.
- Performance and reliability where relevant.
- License and cost constraints for dependencies and services.

Not every review category applies to every documentation-only change; say which checks were skipped.

## 7. Checkpoint

Use the checkpoint template. Record:
- What changed and where.
- Evidence and commit references.
- Checks actually run and results.
- Unverified assumptions, blockers, and risks.
- One next action.

## Status definitions

- **PLANNED:** scoped, not started.
- **ACTIVE:** work is in progress.
- **VERIFIED:** all required acceptance criteria have supporting evidence.
- **BLOCKED:** progress depends on access, information, or another unresolved dependency.
- **DEFERRED:** intentionally postponed with a reason.

A file being created is not proof that the whole product works. A commit SHA proves a commit was returned, not that tests passed.

## Project isolation rules

- Confirm the project and repository name before every write.
- Do not copy one project's source, secrets, customer data, or configuration into another project's workspace.
- Keep shared NEX procedures generic; keep product requirements in that product's own project record.
- If a task could affect multiple repositories, list each separately and get approval for any additional scope.

## Zero-cost gate

Before running an agent, external API, browser automation, deployment, or scheduled job:
1. Identify whether it can incur a charge or consume credits.
2. Verify the current connection and relevant limits.
3. Under the zero-cost policy, do not proceed if cost is unknown or nonzero.
4. Never retry a known insufficient-credit failure without an explicit budget change.
