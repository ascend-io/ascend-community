---
otto:
  rule:
    alwaysApply: true
    description: Guidelines for Otto commands.
---

# Otto Commands

When a user message contains a slash command (e.g., `/audit_rules`):

1. Look for `otto/commands/**/{command_name}.md`
2. Read and execute the instructions in that file
3. If not found, inform the user

Command files should provide clear instructions for what Otto should do, including specific tools or approaches to use.