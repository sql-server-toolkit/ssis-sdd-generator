# ssis-sdd-generator

A Python tool that reads SSIS project artifacts and generates Spec Driven Development (SDD) Markdown files to support Microsoft Fabric migration assessment, technical documentation, and architecture review.

## Objectives

- Analyze SSIS artifacts: `.dtsx`, `.conmgr`, and `.ispac`.
- Extract technical metadata from packages, connections, variables, control flow, data flow, and SQL.
- Generate SDD-oriented Markdown specifications.
- Produce initial Microsoft Fabric migration recommendations and backlog items.

## Project Structure

```text
ssis-sdd-generator/
|-- app/
|-- docs/
|-- specs/
|-- input/
|-- output/
|-- tests/
|-- IMPLEMENTATION_CHECKLIST.md
|-- requirements.txt
`-- README.md
```

## Setup

```bash
python -m pip install -r requirements.txt
```

On Windows, if the `python` alias points to the Microsoft Store launcher, use the full Python path or `py` after confirming it targets a real installation.

## Usage

```bash
python -m app.main ^
  --project-folder ".\input\MySSISProject" ^
  --output-folder ".\output" ^
  --log-level INFO
```

Arguments:

- `--project-folder`: folder containing SSIS files. Defaults to `INPUT_FOLDER` from `.env` or `./input`.
- `--output-folder`: folder where Markdown specs are written. Defaults to `OUTPUT_FOLDER` from `.env` or `./output`.
- `--log-level`: logging level. Defaults to `LOG_LEVEL` from `.env` or `INFO`.

## Supported Input

- `.dtsx`: parsed for package metadata, embedded connections, variables, parameters, control flow, data flow, and SQL commands.
- `.conmgr`: parsed for shared connection metadata.
- `.ispac`: inspected as a zip archive to list package, connection, parameter, and manifest entries.

Markdown generation is currently driven by `.dtsx` packages. `.conmgr` and `.ispac` parsing exists as supporting capability for upcoming project-level aggregation.

## Output

For each package, the tool writes one Markdown file with:

- Context and package metadata.
- Inputs and outputs inferred from connections and SQL.
- Connections with sensitive values masked.
- Parameters and variables.
- Control Flow and Data Flow summaries.
- SQL command blocks.
- Business rules inferred from SQL references.
- Risks and migration blockers.
- Microsoft Fabric target recommendations and migration backlog.

When multiple package specs are generated, `output/index.md` is created as a project index.

Example excerpt:

````markdown
# Spec: SamplePackage

## Connections

| Name | Type | Provider | Server | Database | File |
| --- | --- | --- | --- | --- | --- |
| SourceDb | OLE DB | - | server01 | Sales | - |

## SQL Commands

```sql
INSERT INTO dbo.FactSales SELECT * FROM dbo.StageSales
```
````

## Tests

```bash
python -m unittest discover -v
```

## Development Checks

Optional formatting and lint checks can use the settings in `pyproject.toml`:

```bash
python -m pip install black ruff
python -m black app tests
python -m ruff check app tests
```

## Known Limitations

- SSIS XML variations are handled tolerantly, but more real-world package fixtures are needed.
- `.ispac` contents are inspected but not yet expanded into a full `SSISProject` aggregation flow.
- Business rule inference is currently heuristic and based mainly on SQL/object references.
- Fabric recommendations are initial assessment hints, not final migration design.

## License

MIT
