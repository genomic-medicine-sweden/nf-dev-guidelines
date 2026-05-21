## Publishing

Output files are published via a dedicated `PUBLISH` channel. Every process that produces files for end-users must emit to `ch_publish` using the pattern:

```groovy
emit:
    publish = ch_publish  // channel: [ val(destination), val(value) ]
```

The `{{ repo_name }}` pipeline routes all publish events through the central publish subworkflow defined in `subworkflows/local/publish/main.nf`.
