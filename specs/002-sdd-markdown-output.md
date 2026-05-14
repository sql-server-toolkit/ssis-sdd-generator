# SDD Markdown Output

Each `.dtsx` package produces one Markdown file.

## Sections

- Context
- Objective
- Inputs
- Outputs
- Connections
- Parameters and Variables
- Control Flow
- Data Flow
- SQL Commands
- Business Rules
- Risks and Attention Points
- Implementation Backlog

## Standards

- Markdown tables are used for structured metadata.
- SQL commands are rendered in fenced `sql` blocks.
- Sensitive values in connection strings are masked.
- Missing data is rendered as `_No data detected._`.
- File names are normalized to filesystem-safe Markdown names.
- When multiple package specs are generated, an `index.md` file links them.
