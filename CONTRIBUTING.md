# Contributing to Hacknetics

Thank you for your interest in contributing to Hacknetics. This guide explains how to submit contributions, what we expect from submissions, and how to keep the project consistent.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/Hacknetics.git
cd Hacknetics
```

3. Create a new branch for your changes:

```bash
git checkout -b your-branch-name
```

4. Make your changes, commit, push, and open a pull request against `main`.

## What We Accept

- New tool guides, technique writeups, or cheat sheets relevant to penetration testing and red teaming
- Corrections to existing content (typos, outdated commands, broken links)
- New code snippets, one-liners, or proof-of-concept scripts
- Improvements to page structure, readability, or navigation
- New entries under "Things I Have Pwn'd Before" for software you have exploited

## Content Guidelines

### Writing Style

- Be direct and practical. Lead with commands and examples, follow with brief explanation.
- Write in a cheat-sheet style. Readers should be able to copy-paste commands.
- Use active voice and imperative mood ("Run this command", "Check the output").
- Assume the reader has foundational knowledge of Linux, networking, and security concepts.
- Do not pad content with unnecessary prose. Keep it concise.

### Formatting

- Use `#` for the page title, `##` for major sections, `###` for subsections.
- Wrap all commands and code in fenced code blocks with the appropriate language tag (```bash, ```python, ```powershell, etc.).
- Use tables for comparisons, reference data, and option/flag listings.
- Use `---` horizontal rules to separate major sections.
- Use bullet points (`*` or `-`) for lists.
- Include expected output where it helps clarify what the reader should see.
- Link to external references (HackTricks, GTFOBins, GitHub repos, blog posts) where relevant.

### File Naming

- Use lowercase with hyphens for file names: `my-new-page.md`
- Place files in the appropriate existing directory (e.g., `web/`, `tool-guides/`, `lin-priv-esc/`)
- If a new top-level category is needed, discuss it in an issue first

### SUMMARY.md

If you add a new page, add a corresponding entry to `SUMMARY.md` so it appears in the GitBook table of contents. Follow the existing indentation and nesting structure.

## Pull Request Process

1. Keep pull requests focused. One topic or fix per PR.
2. Write a clear PR title and description explaining what was added or changed and why.
3. Ensure your markdown renders correctly. Preview it locally or use a markdown viewer before submitting.
4. Do not include machine-specific data (real IPs, hostnames, credentials) from non-lab environments.
5. If you reference a CVE or exploit, include the CVE number and at least one reference link.
6. Do not duplicate content that already exists in the repo. Search existing pages before adding new material.

## Reporting Issues

If you find errors, broken links, or outdated content, open an issue with:

- The file path and line number (if applicable)
- A description of the problem
- A suggested fix (if you have one)

## Code of Conduct

All contributors are expected to follow the project [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, professional, and constructive.

## Legal

Hacknetics is released under the [Unlicense](LICENSE). By contributing, you agree that your contributions will be released under the same license.

All content in this repository is intended for authorized security testing and educational purposes only. Do not submit content that encourages or facilitates unauthorized access to systems.
