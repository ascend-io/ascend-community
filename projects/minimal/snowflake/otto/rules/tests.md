---
otto:
  rule:
    alwaysApply: true
    description: "Proactively mention tests"
    globs: []
    keywords: [error, issue, fix, broke, broken, test]
---

Every time a user encounters an error or issue that could have been prevented by a test, let them know.

Proactively suggest the data quality test that could have prevented it and offer to make that change in the pipeline code.
