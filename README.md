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

vars:
  repo_name: my-org/my-pipeline
  repo_url: https://github.com/my-org/my-pipeline
  codespaces_url: https://github.com/my-org/my-pipeline/codespaces
  pre_commit_note: "This repository includes the nf-core pipelines schema docs hook."
  workflow_file: workflows/my-pipeline.nf
  reuse_note: "Follow the DRY (Don't Repeat Yourself) principle."
  modules_note: "Always prefer a module from nf-core or genomic-medicine-sweden over writing a local one. Only add to modules/local/ as a last resort when the use case is too pipeline-specific."

  - file: contributing/publishing.md
  - file: contributing/gpu.md
```

### 2. Add pipeline-specific section files

Create any files referenced in `custom_sections`. Each file contains the section body without a heading (the `## Title` is added by the template from `custom_sections[].title`).

### 3. Add the sync workflow

Add `.github/workflows/sync-guidelines.yml` to the consuming repository.

> **Required repository setting:** go to **Settings → Actions → General → Workflow permissions** and enable **"Allow GitHub Actions to create and approve pull requests"**. Without this the `create-pull-request` step will fail.

> **Required secrets:** the workflow uses the `nf-guidelines-sync-bot` GitHub App to open PRs so that CI is triggered on the resulting PR (PRs opened with the default `GITHUB_TOKEN` do not trigger other workflows). The app must be installed on the consuming repository. Add two secrets under **Settings → Secrets and variables → Actions**: `NF_GUIDELINES_APP_ID` (the numeric app ID) and `NF_GUIDELINES_APP_PRIVATE_KEY` (the PEM private key).



```yaml
name: Sync guidelines

on:
  workflow_dispatch:
  schedule:
    - cron: "0 8 * * *" # daily

permissions:
  contents: write
  pull-requests: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Clone nf-dev-guidelines
        run: |
          git clone --depth 1 --branch main \
            https://github.com/genomic-medicine-sweden/nf-dev-guidelines.git \
            /tmp/nf-dev-guidelines

      - name: Install dependencies
        run: pip install -r /tmp/nf-dev-guidelines/requirements.txt

      - name: Generate CONTRIBUTING.md
        run: |
          python /tmp/nf-dev-guidelines/generator/generate.py \
            --config assets/contribution-guidelines-config.yaml \
            --guidelines /tmp/nf-dev-guidelines \
            --repo-root . \
            --output docs/CONTRIBUTING.md

      - name: Generate table of contents
        run: npx --yes doctoc --github docs/CONTRIBUTING.md

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ secrets.NF_GUIDELINES_APP_ID }}
          private-key: ${{ secrets.NF_GUIDELINES_APP_PRIVATE_KEY }}

      - name: Create pull request
        uses: peter-evans/create-pull-request@v7
        with:
          token: ${{ steps.app-token.outputs.token }}
          commit-message: "docs: update CONTRIBUTING.md from nf-dev-guidelines"
          title: "Update CONTRIBUTING.md from nf-dev-guidelines"
          body: |
            Auto-generated from [nf-dev-guidelines](https://github.com/genomic-medicine-sweden/nf-dev-guidelines).
          branch: update-contributing-guidelines
          delete-branch: true

```

### 4. Disable nf-core `template_strings` lint for the generated file

nf-core's `template_strings` lint check flags any `{{ }}` patterns in the repository as unrendered Jinja2 placeholders. The `contribution-guidelines-config.yaml` file contains `{{ }}` which would cause this check to fail.

Add the following to `.nf-core.yml` in the consuming repository:

```yaml
lint:
  template_strings:
    - assets/contribution-guidelines-config.yaml
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
3. Merge to `main` — consuming repositories will pick up the change on their next daily sync.
