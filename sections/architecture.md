### Architecture & structure

- **Use subworkflows** — Don't add logic to `{{ workflow_file }}` that is specific to a subworkflow. Create new subworkflows as needed under `subworkflows/` and import them into `{{ workflow_file }}`.
- **Reuse over duplication** — {{ reuse_note }}
- **nf-core modules take precedence** — {{ modules_note }}
- **Use and share subworkflows with the GMS community** — subworkflows from [genomic-medicine-sweden/nf-core-modules](https://github.com/genomic-medicine-sweden/nf-core-modules) are intended for use across pipelines within the Genomic Medicine Sweden group. Prefer using and contributing to these rather than writing pipeline-specific code in `subworkflows/local/`. If you think a subworkflow could be useful for other pipelines, consider adding it there instead of `subworkflows/local/`.
