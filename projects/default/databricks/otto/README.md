# Otto Configuration

AI agent customization for this project.

## Structure

| File/Directory | Description |
|----------------|-------------|
| `otto.yaml` | Main Otto configuration (MCP server access) |
| `mcp.yaml` | MCP server definitions (GitHub, MotherDuck) |
| `agents/` | Custom agent personalities |
| `commands/` | Slash command definitions |
| `rules/` | Project-specific rules for Otto |

## Custom Agents

- **Professor Otto** (`agents/professor_otto.md`) - Extended agent for new users with detailed explanations
- **Code Reviewer** (`agents/code_reviewer.md`) - Reviews code changes and provides actionable feedback

## Commands

- `/audit_rules` - Audit project rules against learning principles

## Project Rules

| Rule | Description |
|------|-------------|
| `visualizations` | Guidelines for data visualizations in artifacts |
| `learning` | Guidelines for capturing learnings and improving rules |
| `readme_maintenance` | Guidelines for maintaining README files |
| `commands` | Guidelines for Otto commands |
| `migration` | Guidelines for migrating ETL logic from other platforms |

## MCP Servers

Available MCP servers (configure access in `otto.yaml`):

- **github** - GitHub Copilot MCP (requires `GITHUB_TOKEN`)
- **motherduck** - MotherDuck MCP (requires `MOTHERDUCK_API_KEY`)