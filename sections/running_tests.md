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
