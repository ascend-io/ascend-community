---
otto:
  rule:
    alwaysApply: true
    description: "Ensure correct syntax when using apply_patch tool."
    globs: []
    keywords: []
---

When using the apply_patch() tool call ensure that the final line of the patch is  `*** End Patch`.
Do NOT include a `+` before this line as this will result in an error.
