### Software versioning, changelog and updates

#### Semantic versioning and changelog

Release versioning is maintained according to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and a changelog is maintained according to the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format. Although, for a Nextflow pipeline it can be hard to decide what is a breaking/non-breaking API change.

Bugs fixed between releases belong in the `Fixed` section of the changelog, whereas bug fixes that appeared and were solved in dev should go in the `Changed` section.

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
