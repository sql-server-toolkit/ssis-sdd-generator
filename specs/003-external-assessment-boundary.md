# External Assessment Boundary

This project focuses on generating SDD documentation for SSIS projects.

Platform-specific assessments, such as Microsoft Fabric migration feasibility, are outside the core responsibility of this application. A separate assessment application can consume the generated Markdown or a future structured export.

## Core Responsibilities

- Parse SSIS artifacts.
- Extract package metadata.
- Document connections, variables, parameters, control flow, data flow, and SQL.
- Generate SDD Markdown.
- Produce neutral implementation backlog items.

## Out Of Scope

- Microsoft Fabric target mapping.
- Migration complexity scoring for a specific platform.
- Platform-specific blockers and recommendations.
- Cloud architecture decisions.

## Future Integration

A future assessment application may consume:

- generated Markdown files;
- package metadata from parser output;
- a future JSON export format;
- project-level index files.
