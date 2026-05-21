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
