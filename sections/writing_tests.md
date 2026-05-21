### Writing tests

- Every subworkflow should have tests at `subworkflows/local/<name>/tests/main.nf.test`.
- Snapshot files (`*.nf.test.snap`) are committed alongside tests — update them when outputs change.
- Pipeline-level tests live in `tests/`.
{% if extra_test_notes | default('') %}
{{ extra_test_notes }}
{% endif %}
