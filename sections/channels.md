### Channels

- **Conditional channels**: always initialize to `channel.empty()` before any `if` block that may or may not assign them. Never leave a channel potentially undefined.
