# Public Release Checklist

Use this checklist before distributing a NEX release or publishing a repository copy.

## Contents and licensing

- Confirm the copyright holder and license are correct.
- Review the full Git history, branches, tags, release assets, issues, and pull request discussions for credentials, personal data, private project details, and internal planning material.
- Review included skills and third-party material for redistribution rights and required attribution.
- Keep internal reports, generated private project outputs, account screenshots, and personal notes out of release copies.
- Recheck product support claims against current official documentation.

## Product claims

- Distinguish installer-supported clients from manual or adapter-based use.
- State that NEX is local-first and does not provide a hosted autonomous agent.
- Identify the local MCP tools and what each one can read or generate.
- Do not present a UI/UX checklist as a measured accessibility audit or a conversion guarantee.
- Do not claim tests passed unless the exact release commit has evidence.

## Cost and privacy

- The included local utilities do not call model APIs or NEX-operated servers.
- A connected AI client may send prompts, repository content, and tool results to its provider and may incur provider charges.
- Do not enable hosted workflows, analytics, or package publishing until their current cost and data handling are understood.
- Read [PRIVACY.md](../PRIVACY.md) and [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

## Distribution

- Verify installation instructions on Windows and at least one other operating system.
- Make a clean release copy with only intended files and a clean Git history.
- Use a versioned release and concise change notes.
- Keep the release reproducible and easy to remove.
