---
otto:
  rule:
    alwaysApply: true
---

When generating ANY git commit messages or squash and sync messages, YOU MUST use the Conventional Commits format:

### 🧾 Format
Git commit messages must follow the formatting below:

<type>(optional-scope): concise summary

- The summary must be in **present tense**, imperative mood (e.g. “add logging” not “added”).
- Do **not** end the summary line with punctuation.
- Keep the first line under 72 characters.
- Leave a blank line before any body content.

### ✅ Allowed Types

- `feat`: New feature
- `fix`: Bug fix
- `chore`: Non-code change (e.g. config, formatting)
- `refactor`: Code change that doesn’t add or fix functionality
- `docs`: Documentation update
- `test`: Adding or updating tests
- `perf`: Performance improvements
- `ci`: Changes to CI/CD setup

### 💡 Examples

- `feat(transform): add user-level deduplication step`
- `fix(metadata): correct schema name for staging table`
- `chore: update dbt package versions`
- `docs(readme): clarify pipeline overview`
- `refactor: restructure the DAG for modularity`

If you're unsure which type to use, prefer `feat`, `fix`, or `chore`.
Be specific and useful — think about how this message will help your future self or your teammates scanning the commit log.

