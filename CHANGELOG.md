# Changelog

## Unreleased

## v1.0.0

Initial release.

### Sections

All sections listed below are available. Include them by name in the `sections:` list of your `repo-config.yaml`.

| Section | Heading level | Description |
|---|---|---|
| `contribution_workflow` | `###` | Fork/PR contribution steps |
| `pull_requests` | `####` | PR checklist and conventions |
| `review` | `#####` | Code review expectations |
| `versioning` | `###` | Semantic versioning, changelog, nf-core template sync |
| `developer_setup` | `###` | Local installation, pre-commit, Codespaces |
| `running_tests` | `###` | nf-test command, lint tests, pipeline tests |
| `coding_conventions_header` | `##` | "Coding conventions" section header |
| `architecture` | `###` | Pipeline structure and module reuse rules |
| `adding_a_step` | `###` | Step-by-step coding standards checklist |
| `channels` | `###` | Channel conditional-existence rules |
| `parameters` | `###` | params access policy |
| `configuration` | `###` | Config file conventions and resource requirements |
| `writing_tests` | `###` | nf-test location, snapshot files, pipeline tests |
| `style` | `###` | take:/emit: comments, channel declaration style |

### Required variables

These must be present in `vars:` when the corresponding section is included.

| Variable | Required by |
|---|---|
| `repo_name` | `contribution_workflow`, `architecture`, `coding_conventions_header` |
| `repo_url` | `contribution_workflow`, `developer_setup` |
| `codespaces_url` | `developer_setup` |
| `pre_commit_note` | `developer_setup` |
| `workflow_file` | `architecture` |
| `reuse_note` | `architecture` |
| `modules_note` | `architecture` |

### Optional variables

These use `| default('')` and produce no output when absent.

| Variable | Used in | Description |
|---|---|---|
| `pr_title_conventions_section` | `pull_requests` | Full markdown block for PR title conventions |
| `nf_test_examples` | `running_tests` | Additional nf-test tag/path examples |
| `additional_test_notes` | `running_tests` | Additional notes block (e.g. NOTE callout) |
| `extra_test_notes` | `writing_tests` | Extra bullet points for writing tests |
| `extra_style_notes` | `style` | Pipeline-specific style bullet points |

### Migration notes

_Initial release — no migration required._
