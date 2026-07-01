## General

### Contribution workflow

If you'd like to write some code for {{ repo_name }}, the standard workflow is as follows:

1. Check that there isn't already an issue about your idea in the [{{ repo_name }} issues]({{ repo_url }}/issues) to avoid duplicating work. If there isn't one already, please create one so that others know you're working on this
2. [Fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) the [{{ repo_name }} repository]({{ repo_url }}) to your GitHub account
3. Make the necessary changes / additions within your forked repository following [Pipeline conventions](#pipeline-contribution-conventions)
4. Use `nf-core pipelines schema build` and add any new parameters to the pipeline JSON schema (requires [nf-core tools](https://github.com/nf-core/tools) >= 1.10).
5. Submit a Pull Request against the `dev` branch and wait for the code to be reviewed and merged

If you're not used to this workflow with git, you can start with some [docs from GitHub](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests) or even their [excellent `git` resources](https://try.github.io/).

#### Pull Requests

When opening a pull request to suggest changes to the code, please make sure to follow the [Pipeline contribution conventions](#pipeline-contribution-conventions) for the code and to fill in the necessary information in the pull request template as well as address all points in the `PR checklist`.
{% if pr_title_conventions_section | default('') %}

{{ pr_title_conventions_section }}
{% endif %}

##### Review

When reviewing a PR, make sure to check that:

- The code follows the [Pipeline contribution conventions](#pipeline-contribution-conventions).
- The information in the PR (and related issue) is clear and sufficient to understand the change and the motivation for it - title, description and entry in `CHANGELOG.md`, if applicable.
- All the items in the `PR checklist` have been addressed, the changes are well documented and the tests are passing.

Be positive and constructive in your review, and whenever possible offer suggestions for improvement rather than just pointing out issues.

### Software versioning, changelog and updates

#### Semantic versioning and changelog

Release versioning is maintained according to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and a changelog is maintained according to the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format. Although, for a Nextflow pipeline it can be hard to decide what is a breaking/non-breaking API change.

{% if extra_semantic_versioning_notes | default('') %}
{{ extra_semantic_versioning_notes }}

{% endif %}

##### Patch

:warning: Only in the unlikely and regretful event of a release happening with a bug.

- Make a new branch `patch` based on `upstream/main` or `upstream/master`.
- Fix the bug, and bump version (X.Y.Z+1).
- Open a pull-request from `patch` to `main`/`master` with the changes.

#### Nextflow version bumping

If you are using a new feature from core Nextflow, you may bump the minimum required version of nextflow in the pipeline with: `nf-core pipelines bump-version --nextflow . [min-nf-version]`

#### Update nf-core template

Since this is not an nf-core pipeline, the nf-core template is not automatically updated in the `TEMPLATE` branch. Follow these steps to update the template:

1. Update the `TEMPLATE` branch by running `nf-core pipelines sync`. Fix any merge conflicts.
2. Open a PR to merge the `TEMPLATE` branch into `dev` to update the template files in the main codebase.

### Developer setup

#### Installation and dependencies for development

In order to run the pipeline, develop and test your changes locally, we recommend that you set up:

- A conda environment with `nextflow`, `nf-core` tools and `nf-test`. For this, follow the instructions from the [nf-core documentation](https://nf-co.re/docs/nf-core-tools/cli/installation#install-with-conda) and install `nf-test` from bioconda or by following the [nf-test installation instructions](https://www.nf-test.com/installation/). Additional information about [installation of nf-core dependencies](https://nf-co.re/docs/usage/getting_started/installation/) is also available, if needed.
- Install Docker (https://www.docker.com/products/docker-desktop/) and make sure the daemon is running when you want to run the tests locally.

Make sure to [test your setup](https://nf-co.re/docs/usage/introduction#how-to-run-a-pipeline) with `-profile test` before running the workflow on actual data.

Additionally, pre-commit hooks are set up to automatically check the code and generate parameters documentation when committing. To install the pre-commit hooks, run `pre-commit install` in the root of the repository. {{ pre_commit_note }}

#### GitHub Codespaces

This repo includes a devcontainer configuration which will create a GitHub Codespaces for Nextflow development! This is an online developer environment that runs in your browser, complete with VSCode and a terminal.

To get started:

- Open the repo in [Codespaces]({{ codespaces_url }})
- Tools installed
  - nf-core
  - Nextflow

Devcontainer specs:

- [DevContainer config](.devcontainer/devcontainer.json)

### Running tests

You have the option to test your changes locally by running the pipeline. For receiving warnings about process selectors and other `debug` information, it is recommended to use the debug profile. Execute all the tests with the following command:

```bash
nf-test test --profile debug,test,docker --verbose
```

{% if nf_test_examples | default('') %}
{{ nf_test_examples }}

{% endif %}
{% if additional_test_notes | default('') %}
{{ additional_test_notes }}

{% endif %}
When you create a pull request with changes, [GitHub Actions](https://github.com/features/actions) will run automatic tests.
Typically, pull-requests are only fully reviewed when these tests are passing, though of course we can help out before then.

There are typically two types of tests that run:

#### Lint tests

`nf-core` has a [set of guidelines](https://nf-co.re/developers/guidelines) which all pipelines must adhere to.
To enforce these and ensure that all pipelines stay in sync, nf-core has developed a helper tool which runs checks on the pipeline code. This is in the [nf-core/tools repository](https://github.com/nf-core/tools) and once installed can be run locally with the `nf-core pipelines lint <pipeline-directory>` command.

If any failures or warnings are encountered, please follow the listed URL for more documentation.

#### Pipeline tests

This pipeline is set up with a minimal set of test-data.
`GitHub Actions` then runs the pipeline on this data to ensure that it exits successfully.
If there are any test failures then the automated check has status set to fail.
These tests are run both with the latest available version of `Nextflow` and also the minimum required version that is stated in the pipeline code.
