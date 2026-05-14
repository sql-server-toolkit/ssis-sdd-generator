# SSIS Input Analysis

The generator supports three SSIS artifact types.

## `.dtsx`

Package files are parsed as XML. The parser extracts:

- package metadata;
- embedded connection managers;
- variables and parameters;
- executable tasks;
- precedence constraints;
- data flow components;
- SQL command properties.

The parser uses local XML names so SSIS namespace prefixes can vary.

## `.conmgr`

Connection manager files are parsed as XML. The parser extracts connection name, type, provider, server, database, file path, and masked connection string.

## `.ispac`

Deployment archives are inspected as zip files. The parser lists package files, connection managers, project parameter files, manifest files, and raw entries. Full project aggregation is a later implementation step.

## Error Handling

Invalid files should fail at the file level and allow the CLI to continue processing other packages whenever possible.
