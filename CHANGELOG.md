# Changelog

## Unreleased

### Added

- `generator/generate.py` — Python CLI that reads a repo-specific YAML config, renders shared and custom sections as Jinja2 templates, and writes `CONTRIBUTING.md`. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `sections/general.md` — Shared section covering contribution workflow, pull requests, review process, software versioning, developer setup, and running tests. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `sections/coding_conventions.md` — Shared section covering architecture & structure, adding a new step, channels, parameters, configuration, writing tests, and style guidelines. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `templates/CONTRIBUTING.md.j2` — Jinja2 document template that assembles the final output from rendered sections. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `requirements.txt` — Python dependencies (`click`, `jinja2`, `pyyaml`). [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `README.md` — Documentation for consuming repositories: setup instructions, template variables reference, and a guide for adding new shared sections. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `Makefile` — Convenience targets for generating, previewing, and updating the test file locally. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `.github/workflows/validate.yml` — CI workflow that runs the generator against both test configs, diffs the default output against a golden file, and lints both outputs for formatting issues. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `.github/test-config.yaml` / `.github/test-config-full.yaml` — Minimal and full test configs used by CI. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `.github/expected-output.md` — Golden file for CI diff validation. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- `.github/CODEOWNERS` — Code ownership configuration. [#1](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/1)
- Automatic calendar versioning releases [#6](https://github.com/genomic-medicine-sweden/nf-dev-guidelines/pull/6)