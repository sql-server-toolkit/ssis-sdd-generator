# SDD Generation Methodology

1. Collect SSIS inputs: `.dtsx`, `.conmgr`, and `.ispac` artifacts.
2. Run the generator against the project input folder.
3. Review generated SDD package specifications with package owners.
4. Validate extracted connections, variables, parameters, SQL, control flow, and data flow metadata.
5. Confirm inferred inputs, outputs, and business rules.
6. Review risks and attention points.
7. Convert generated backlog items into implementation tasks.

The generated SDD should describe the current SSIS project accurately without deciding the target modernization platform.
