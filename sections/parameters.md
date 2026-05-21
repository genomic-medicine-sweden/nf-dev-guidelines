### Parameters

- `params` must only be accessed in the main unnamed workflow (`workflow` in `main.nf`). Subworkflows and named workflows receive all values as explicit `val_*` arguments. Never reference `params` directly inside a subworkflow.
- Parameters should be initialised/defined with default values within the `params` scope in `nextflow.config`. Don't hardcode values that a user might reasonably want to change. Once added, run `nf-core pipelines schema build` to register them in `nextflow_schema.json`.
