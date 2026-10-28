# NEX Privacy and Data-Handling Notice

**Effective date:** 2026-10-28

This notice describes the NEX repository and the software included in it. NEX is currently distributed as source files and local utilities; this repository does not operate a NEX-hosted account, website, or service.

## Information handled by NEX software

The included utilities run on the user's computer:

- The skill installer reads skill files from the local repository and copies them to the destination selected by the user. If the user chooses to replace an existing skill, it may keep a timestamped local backup.
- The Agent Factory reads a JSON file selected by the user and writes draft Markdown files to the output directory selected by the user.
- The local MCP server receives tool requests from the AI client running on the same computer. It reads the requested NEX skill or creates draft text in memory. It makes no network or model API calls and does not save tool requests or generated results.

The current NEX utilities do not send usage telemetry, analytics, account details, or user content to a NEX-operated server. NEX does not set or read browser cookies. Files created or copied by the local utilities remain under the user's control; the user can remove them, including any backups.

## Other services

GitHub processes repository access, downloads, and activity under GitHub's own terms and privacy notice. If a user connects NEX to an AI client, that client may send prompts, repository content, and tool results to its model provider. The provider's terms, settings, retention practices, and charges apply to that use. NEX does not control those services.

Do not put secrets, credentials, or unnecessary personal information in prompts, generated files, public issues, or repository contributions.

## Questions

For a privacy question about NEX's included software, contact the repository owner through the owner's GitHub profile. Do not post private or sensitive information in a public issue.

## Scope and changes

This notice covers the software currently included in this repository. It does not cover modified copies, third-party clients or providers, or future hosted services. If NEX adds telemetry, accounts, remote hosting, or another data-collection feature, this notice must be reviewed and updated before that feature is released.

This is a plain-language description of current software behavior, not a statement that every organization or deployment meets every legal requirement.