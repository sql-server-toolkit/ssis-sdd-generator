# Fabric Migration Assessment

The Fabric migration assessment is generated per package.

## Complexity

Complexity is classified as `Low`, `Medium`, or `High` using package metadata volume and blocker count:

- task count;
- data flow count;
- SQL command count;
- migration blocker count.

## Target Mapping

- SSIS orchestration maps to Data Factory Pipelines.
- Data Flow Tasks map to Dataflows Gen2 or Notebooks.
- SQL workloads map to Warehouse or Lakehouse.
- Script Tasks map to Notebooks or custom activities.
- File and FTP/SFTP tasks map to Data Factory copy or storage activities.

## Blockers

The initial blocker list includes:

- script tasks;
- custom or COM tasks;
- custom or script data flow components;
- dynamic SQL;
- local files and shared folder dependencies.

## Output

The assessment produces:

- complexity;
- target patterns;
- effort estimate;
- blockers;
- component-level recommendations;
- migration backlog items.
