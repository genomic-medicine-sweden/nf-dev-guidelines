### Configuration

- Process-level options go in `conf/subworkflows/<subworkflow_name>.config`, not inline in the subworkflow `.nf` file.
- Use module configs strictly for defining `ext.args`, `ext.args2`, and `ext.prefix`. Do not place complex decision-making, conditions or workflow behaviour logic there.
- Conditional behavior (e.g. save as CRAM vs BAM) is handled in the subworkflow via `channel.empty()` gating — not via config-level flags.
- Process resource requirements (CPUs / memory / time) go in `conf/base.config` using `withLabel:` selectors so they can be shared across processes. Use `${task.cpus}` and `${task.memory}` in `script:` blocks to apply them dynamically.
