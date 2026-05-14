# Migration POC Methodology

1. Collect SSIS inputs: `.dtsx`, `.conmgr`, and `.ispac` artifacts.
2. Run the generator against the project input folder.
3. Review generated SDD package specifications with package owners.
4. Validate extracted connections, variables, SQL, control flow, and data flow metadata.
5. Evaluate Microsoft Fabric target patterns:
   - Data Factory Pipelines for orchestration.
   - Dataflows Gen2 for visual transformations.
   - Notebooks for custom transformation logic.
   - Lakehouse or Warehouse for analytical storage and SQL workloads.
6. Review blockers:
   - Script tasks and script components.
   - Custom or COM components.
   - Dynamic SQL.
   - Local file or shared folder dependencies.
7. Produce migration backlog from generated recommendations and owner review.
