## Coding conventions

To make the `{{ repo_name }}` code and processing logic more understandable for new contributors and to ensure quality, we semi-standardise the way the code and other contributions are written.

### Architecture & structure

- **Use subworkflows** — Don't add logic to `{{ workflow_file }}` that is specific to a subworkflow. Create new subworkflows as needed under `subworkflows/` and import them into `{{ workflow_file }}`.
- **Reuse over duplication** — {{ reuse_note }}
- **nf-core modules take precedence** — {{ modules_note }}
- **Use and share subworkflows with the GMS community** — subworkflows from [genomic-medicine-sweden/nf-core-modules](https://github.com/genomic-medicine-sweden/nf-core-modules) are intended for use across pipelines within the Genomic Medicine Sweden group. Prefer using and contributing to these rather than writing pipeline-specific code in `subworkflows/local/`. If you think a subworkflow could be useful for other pipelines, consider adding it there instead of `subworkflows/local/`.

### Adding a new step

If you wish to contribute a new step, please use the following coding standards:

1. Define the corresponding input channel into your new process from the expected previous process channel.
2. Write the process block (see below).
3. Define the output channel if needed (see below).
4. Add any new parameters to `nextflow.config` with a default (see below).
5. Add any new parameters to `nextflow_schema.json` with help text (via the `nf-core pipelines schema build` tool).
6. Add sanity checks and validation for all relevant parameters.
7. Perform local tests to validate that the new code works as expected.
8. If applicable, add a new test in the `tests` directory.
9. Update MultiQC config `assets/multiqc_config.yml` so relevant suffixes, file name clean up and module plots are in the appropriate order. If applicable, add a [MultiQC](https://multiqc.info/) module.
10. Add a description of the output files and if relevant any appropriate images from the MultiQC report to `docs/output.md`.

### Channels

- **Conditional channels**: always initialize to `channel.empty()` before any `if` block that may or may not assign them. Never leave a channel potentially undefined.

### Parameters

- `params` must only be accessed in the main unnamed workflow (`workflow` in `main.nf`). Subworkflows and named workflows receive all values as explicit `val_*` arguments. Never reference `params` directly inside a subworkflow.
- Parameters should be initialised/defined with default values within the `params` scope in `nextflow.config`. Don't hardcode values that a user might reasonably want to change. Once added, run `nf-core pipelines schema build` to register them in `nextflow_schema.json`.

### Configuration

- Process-level options go in `conf/subworkflows/<subworkflow_name>.config`, not inline in the subworkflow `.nf` file.
- Use module configs strictly for defining `ext.args`, `ext.args2`, and `ext.prefix`. Do not place complex decision-making, conditions or workflow behaviour logic there.
- Conditional behavior (e.g. save as CRAM vs BAM) should be handled in the subworkflow — not via config-level flags.
- Process resource requirements (CPUs / memory / time) go in `conf/base.config` using `withLabel:` selectors so they can be shared across processes. Use `${task.cpus}` and `${task.memory}` in `script:` blocks to apply them dynamically.

### Writing tests

- Every subworkflow should have tests at `subworkflows/local/<name>/tests/main.nf.test`.
- Snapshot files (`*.nf.test.snap`) are committed alongside tests — update them when outputs change.
- Pipeline-level tests live in `tests/`.
{% if extra_test_notes | default('') %}
{{ extra_test_notes }}
{% endif %}

### Style

- Both `take:` and `emit:` block entries require an inline type comment. Use `name // type: [mandatory|optional] description` for `take:` and `name = value // channel: [type description]` for `emit:`. Always include the comment — never leave an entry uncommented.

  ```groovy
  take:
    ch_vcf                // channel: [mandatory] [ val(meta), path(vcf) ]
    ch_reduced_penetrance // channel: [optional]  [ path(penetrance) ]
    val_aligner           // string:  [mandatory] aligner name (bwa/bwamem2/bwameme)
    process_with_sort     // Boolean

  emit:
    vcf     = ch_vcf      // channel: [ val(meta), path(vcf) ]
    publish = ch_publish  // channel: [ val(destination), val(value) ]
  ```

- Use `ch_* = <...>` to declare a new channel. Avoid using `.set { ch_* }`.
{% if extra_style_notes | default('') %}
{{ extra_style_notes }}
{% endif %}
