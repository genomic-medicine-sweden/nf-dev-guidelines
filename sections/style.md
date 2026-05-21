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
