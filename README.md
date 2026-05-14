# ssis-sdd-generator

A Python tool that reads SSIS project artifacts and generates Spec Driven Development (SDD) Markdown files for technical documentation, implementation planning, and architecture review.

## Objectives

- Analyze SSIS artifacts: `.dtsx`, `.conmgr`, and `.ispac`.
- Extract technical metadata from packages, connections, variables, control flow, data flow, and SQL.
- Generate SDD-oriented Markdown specifications.
- Produce project-level SDD documentation and implementation backlog items.

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

Create a dedicated virtual environment for the application:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

After activation, all commands should be executed with the environment's `python`.

If PowerShell blocks activation scripts, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Windows, if the `python` alias points to the Microsoft Store launcher, use the Python launcher instead:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Usage

PowerShell:

```powershell
python -m app.main `
  --ssis-folder "C:\SSIS\MySSISProject" `
  --output-folder ".\output" `
  --log-level INFO
```

Single-line PowerShell command:

```powershell
python -m app.main --ssis-folder "C:\SSIS\MySSISProject" --output-folder ".\output" --log-level INFO
```

If you are using `cmd.exe`, use `^` for line continuation:

```cmd
python -m app.main ^
  --ssis-folder "C:\SSIS\MySSISProject" ^
  --output-folder ".\output" ^
  --log-level INFO
```

Arguments:

- `--ssis-folder`: folder where the SSIS project is located. Accepts absolute or relative paths.
- `--project-folder`: deprecated alias for `--ssis-folder`.
- `--output-folder`: folder where Markdown specs are written. Defaults to `OUTPUT_FOLDER` from `.env` or `./output`.
- `--log-level`: logging level. Defaults to `LOG_LEVEL` from `.env` or `INFO`.

You do not need to copy the SSIS project into this repository. Point `--ssis-folder` directly to the folder where the SSIS files already are.

## Supported Input

- `.dtsx`: parsed for package metadata, embedded connections, variables, parameters, control flow, data flow, and SQL commands.
- `.conmgr`: parsed for shared connection metadata.
- `.ispac`: inspected as a zip archive to list package, connection, parameter, and manifest entries.

Markdown generation is currently driven by `.dtsx` packages. `.conmgr` and `.ispac` parsing exists as supporting capability for upcoming project-level aggregation.

## Output

For each execution, the tool creates a timestamped folder inside `--output-folder`:

```text
output/
`-- MySSISProject_20260514_153045/
    |-- PackageA.md
    |-- PackageB.md
    |-- index.md
    |-- project.json
    `-- packages/
        |-- PackageA.json
        `-- PackageB.json
```

The folder name is composed of:

- the SSIS project folder name;
- execution date;
- execution time.

For each package, the tool writes one Markdown file inside that execution folder with:

- Specification metadata.
- Package purpose.
- Execution contract.
- Technical inventory.
- Data contract.
- Control Flow specification.
- Data Flow specification.
- SQL specification.
- Business rules inferred from package metadata.
- Operational requirements.
- Risks, gaps, and open questions.
- Implementation backlog for review and follow-up work.

When multiple package specs are generated, `index.md` is created inside the execution folder as a project index.

The tool also writes canonical JSON artifacts:

- `project.json`: deterministic project-level extraction result.
- `packages/*.json`: deterministic package-level extraction result.

These JSON files are intended to be the stable input for future AI-assisted SDD enrichment or other external analysis tools.

## Canonical JSON Contract

`project.json` contains:

- `schema_version`;
- generation metadata;
- project name and paths;
- execution summary;
- generated artifacts;
- parsed package payloads.

Package JSON files contain the parser output for each package, including:

- package metadata;
- connections;
- parameters;
- variables;
- control flow tasks;
- data flow components;
- SQL commands;
- warnings and raw properties.

Example excerpt:

````markdown
# SDD: SamplePackage

## 4. Technical Inventory

### 4.1 Connections

| Name     | Type   | Provider | Server   | Database | File |
| -------- | ------ | -------- | -------- | -------- | ---- |
| SourceDb | OLE DB | -        | server01 | Sales    | -    |

## 8. SQL Specification

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
- Platform-specific assessments, such as Microsoft Fabric migration analysis, are intentionally out of scope for this application and should be handled by a separate consumer of the generated SDD.

## License

MIT
