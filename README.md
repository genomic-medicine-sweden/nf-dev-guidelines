# nf-dev-guidelines

Centralized developer guidelines for Nextflow pipelines in the Genomic Medicine Sweden group. Consuming repositories pull from the `main` branch of this repo, compose shared sections with pipeline-specific content, and generate a `CONTRIBUTING.md`.

## How it works

1. This repository owns shared section files (`sections/`), a Jinja2 template (`templates/`), and the generator script (`generator/generate.py`).
2. Each consuming repository contains a `repo-config.yaml` and pipeline-specific section files.
3. A GitHub Actions workflow in the consuming repository clones the `main` branch of this repo, runs the generator, and opens a PR if the output changed.

## Repository structure

```
nf-dev-guidelines/
├── sections/           # Shared reusable markdown sections (Jinja2 templates)
├── templates/          # CONTRIBUTING.md.j2 — the main document template
├── generator/          # generate.py — the generator script
├── requirements.txt    # Python dependencies (jinja2, pyyaml)
└── .github/
    ├── test-config.yaml        # Used by CI to validate the generator
    └── workflows/
        └── validate.yml
```

## Consuming repository setup

### 1. Add `assets/contribution-guidelines-config.yaml`

Create this file in the consuming repository:

```yaml
title: My Pipeline Contributing Guide

intro: |
  My pipeline does X, Y, Z.

sections:
  - general
  - coding_conventions
  - file: contributing/publishing.md
  - file: contributing/gpu.md

vars:
  repo_name: my-org/my-pipeline
  repo_url: https://github.com/my-org/my-pipeline
  codespaces_url: https://github.com/my-org/my-pipeline/codespaces
  pre_commit_note: "This repository includes the nf-core pipelines schema docs hook."
  workflow_file: workflows/my-pipeline.nf
  reuse_note: "Follow the DRY (Don't Repeat Yourself) principle."
  modules_note: "Always prefer a module from nf-core or genomic-medicine-sweden over writing a local one. Only add to modules/local/ as a last resort when the use case is too pipeline-specific."
```

### 2. Add pipeline-specific section files

Create any files referenced as `file:` entries in `sections:` (e.g. `contributing/publishing.md` above). Each file is rendered as a Jinja2 template with the same `vars:` available to the shared sections, and is inserted as-is at that position in the document.

### 3. Add the sync workflow

Add `.github/workflows/sync-guidelines.yml` to the consuming repository. This calls the [reusable workflow](.github/workflows/sync.yml) hosted in this repo, so the actual sync logic lives here — future improvements (bugfixes, new steps) reach every consuming repository automatically, with no changes needed on their side.

> **Required repository setting:** go to **Settings → Actions → General → Workflow permissions** and enable **"Allow GitHub Actions to create and approve pull requests"**. Without this the `create-pull-request` step will fail.

> **Required secrets:** the workflow uses the `nf-guidelines-sync-bot` GitHub App to open PRs so that CI is triggered on the resulting PR (PRs opened with the default `GITHUB_TOKEN` do not trigger other workflows). The app must be installed on the consuming repository. Add two secrets under **Settings → Secrets and variables → Actions**: `NF_GUIDELINES_APP_ID` (the numeric app ID) and `NF_GUIDELINES_APP_PRIVATE_KEY` (the PEM private key), then pass them on with `secrets: inherit` as shown below.

```yaml
name: Sync guidelines

on:
  workflow_dispatch:
  schedule:
    - cron: "0 8 * * *" # daily

jobs:
  sync:
    uses: genomic-medicine-sweden/nf-dev-guidelines/.github/workflows/sync.yml@main
    secrets: inherit
```

Only needed if your repo doesn't use the defaults (`assets/contribution-guidelines-config.yaml` and `docs/CONTRIBUTING.md`):

```yaml
    uses: genomic-medicine-sweden/nf-dev-guidelines/.github/workflows/sync.yml@main
    with:
      config-path: path/to/config.yaml
      output-path: path/to/CONTRIBUTING.md
    secrets: inherit
```

## Template variables reference

Variables are passed via `vars:` in `repo-config.yaml` and are available to all section files as Jinja2 variables.

### Required by default sections

| Variable | Used in | Description |
|---|---|---|
| `repo_name` | `contribution_workflow`, `architecture`, `coding_conventions_header` | Full repo name, e.g. `genomic-medicine-sweden/nallo` |
| `repo_url` | `contribution_workflow`, `developer_setup` | Full GitHub URL |
| `codespaces_url` | `developer_setup` | GitHub Codespaces URL |
| `pre_commit_note` | `developer_setup` | Pipeline-specific pre-commit hook description sentence |
| `workflow_file` | `architecture` | Main workflow file, e.g. `workflows/nallo.nf` |
| `reuse_note` | `architecture` | One-sentence description of the reuse-over-duplication principle |
| `modules_note` | `architecture` | One-sentence description of the nf-core modules preference |

### Optional (used with `| default('')`)

| Variable | Used in | Description |
|---|---|---|
| `pr_title_conventions_section` | `pull_requests` | Full markdown block for PR title conventions (#### heading + content) |
| `nf_test_examples` | `running_tests` | Additional nf-test tag/path examples after the main command |
| `additional_test_notes` | `running_tests` | Additional notes block (e.g. GitHub-flavored NOTE callout about test profiles) |
| `extra_test_notes` | `writing_tests` | Extra bullet points for the writing tests section |
| `extra_style_notes` | `style` | Additional pipeline-specific style bullet points |

## Adding a new shared section

1. Create `sections/<name>.md` — a Jinja2 template starting with the appropriate markdown heading.
2. Update `sections/` variable documentation in this README if it introduces new template variables.
3. Merge to `main`. New sections are opt-in: existing consuming repositories won't render it until they add `<name>` to `sections:` in their own config.

## Removing a shared section

Deleting a `sections/*.md` file that a consuming repository still references in `sections:` does not break their sync workflow: the generator prints a warning to stderr, skips the section, and still generates the rest of the document, so the daily sync PR opens as usual. Reviewing that PR's diff (the section's content disappearing) is the signal for the pipeline maintainer to remove the stale entry from their `sections:` list.
