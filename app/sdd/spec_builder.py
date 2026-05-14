from app.sdd.templates import PACKAGE_TEMPLATE


class SpecBuilder:

    def build_package_spec(self, package_data: dict) -> str:
        return PACKAGE_TEMPLATE.format(
            package_name=package_data["package_name"],
            specification_metadata=self._specification_metadata(package_data),
            package_purpose=self._package_purpose(package_data),
            execution_contract=self._execution_contract(package_data),
            inputs=self._inputs(package_data),
            outputs=self._outputs(package_data),
            source_to_target_mapping=self._source_to_target_mapping(package_data),
            connections=self._connections(package_data),
            parameters=self._parameters(package_data),
            variables=self._variables(package_data),
            control_flow=self._control_flow(package_data),
            data_flow=self._data_flow(package_data),
            sql_commands=self._sql_commands(package_data),
            business_rules=self._business_rules(package_data),
            operational_requirements=self._operational_requirements(package_data),
            risks=self._risks(package_data),
            implementation_backlog=self._implementation_backlog(package_data),
        )

    def _specification_metadata(self, package_data: dict) -> str:
        rows = [
            ("Spec type", "SQL Server Integration Services package SDD"),
            ("Package name", package_data.get("package_name")),
            ("File path", package_data.get("file_path")),
            ("Package ID", package_data.get("package_id")),
            ("Version", package_data.get("version")),
            ("Creator", package_data.get("creator")),
            ("Creation date", package_data.get("creation_date")),
            ("Generated status", "Draft generated from SSIS metadata"),
        ]
        return self._definition_table(rows)

    def _package_purpose(self, package_data: dict) -> str:
        package_name = package_data.get("package_name")
        task_count = len(package_data.get("tasks", []))
        data_flow_count = len(package_data.get("data_flows", []))
        sql_count = len(package_data.get("sql_commands", []))

        return (
            f"This specification documents the SSIS package `{package_name}` as extracted from "
            "the source project. The functional purpose must be confirmed with the package owner.\n\n"
            f"Detected scope: {task_count} control flow task(s), {data_flow_count} data flow(s), "
            f"{sql_count} SQL command(s)."
        )

    def _execution_contract(self, package_data: dict) -> str:
        parameter_rows = [
            [
                parameter.get("name"),
                parameter.get("data_type") or "-",
                self._safe_value(parameter.get("value")),
                parameter.get("required") or "-",
                parameter.get("sensitive") or "-",
            ]
            for parameter in package_data.get("parameters", [])
        ]
        required_connections = [
            [connection.get("name"), connection.get("connection_type") or "-", self._connection_location(connection)]
            for connection in package_data.get("connections", [])
        ]

        return (
            "### Runtime Parameters\n\n"
            + self._table(["Name", "Type", "Default", "Required", "Sensitive"], parameter_rows)
            + "\n\n### Required Connections\n\n"
            + self._table(["Name", "Type", "Location"], required_connections)
            + "\n\n### Preconditions\n\n"
            + self._preconditions(package_data)
            + "\n\n### Postconditions\n\n"
            + self._postconditions(package_data)
        )

    def _inputs(self, package_data: dict) -> str:
        inputs = []
        for connection in package_data.get("connections", []):
            if self._looks_like_input(connection):
                inputs.append(
                    [
                        connection.get("name"),
                        connection.get("connection_type"),
                        self._connection_location(connection),
                    ]
                )

        return self._table(["Name", "Type", "Location"], inputs)

    def _outputs(self, package_data: dict) -> str:
        outputs = []
        for command in package_data.get("sql_commands", []):
            if command.get("statement_type") == "DML":
                sql = command.get("sql", "").strip().upper()
                if sql.startswith(("INSERT", "UPDATE", "DELETE", "MERGE")):
                    outputs.append(
                        [
                            command.get("source"),
                            ", ".join(command.get("referenced_objects", [])) or "-",
                            command.get("property"),
                        ]
                    )

        return self._table(["Source", "Object", "Property"], outputs)

    def _source_to_target_mapping(self, package_data: dict) -> str:
        rows = []
        for flow in package_data.get("data_flows", []):
            sources = []
            destinations = []
            transformations = []
            for component in flow.get("components", []):
                component_name = component.get("name")
                component_type = component.get("component_type")
                if component_type == "Source":
                    sources.append(component_name)
                elif component_type == "Destination":
                    destinations.append(component_name)
                else:
                    transformations.append(component_name)

            rows.append(
                [
                    flow.get("name"),
                    ", ".join(sources) or "-",
                    ", ".join(transformations) or "-",
                    ", ".join(destinations) or "-",
                ]
            )

        return self._table(["Data flow", "Sources", "Transformations", "Destinations"], rows)

    def _connections(self, package_data: dict) -> str:
        rows = []
        for connection in package_data.get("connections", []):
            rows.append(
                [
                    connection.get("name"),
                    connection.get("connection_type"),
                    connection.get("provider") or "-",
                    connection.get("server") or "-",
                    connection.get("database") or "-",
                    connection.get("file_path") or "-",
                ]
            )

        table = self._table(
            ["Name", "Type", "Provider", "Server", "Database", "File"],
            rows,
        )

        details = []
        for connection in package_data.get("connections", []):
            if connection.get("connection_string"):
                details.append(
                    f"- `{connection.get('name')}`: `{connection.get('connection_string')}`"
                )

        return table if not details else f"{table}\n\n### Connection Strings\n\n" + "\n".join(details)

    def _parameters(self, package_data: dict) -> str:
        parameter_rows = [
            [
                parameter.get("name"),
                parameter.get("data_type") or "-",
                self._safe_value(parameter.get("value")),
                parameter.get("required") or "-",
                parameter.get("sensitive") or "-",
            ]
            for parameter in package_data.get("parameters", [])
        ]

        return self._table(["Name", "Type", "Default", "Required", "Sensitive"], parameter_rows)

    def _variables(self, package_data: dict) -> str:
        variable_rows = [
            [
                variable.get("name"),
                variable.get("namespace") or "-",
                variable.get("data_type") or "-",
                self._safe_value(variable.get("value")),
                variable.get("scope") or "-",
                variable.get("expression") or "-",
            ]
            for variable in package_data.get("variables", [])
        ]

        return self._table(["Name", "Namespace", "Type", "Value", "Scope", "Expression"], variable_rows)

    def _control_flow(self, package_data: dict) -> str:
        rows = []
        for task in package_data.get("tasks", []):
            rows.append(
                [
                    task.get("name"),
                    task.get("properties", {}).get("category") or task.get("task_type"),
                    task.get("parent") or "-",
                    str(len(task.get("precedence_constraints", []))),
                    ", ".join(task.get("properties", {}).get("child_tasks", [])) or "-",
                    task.get("description") or "-",
                ]
            )

        return self._table(
            ["Name", "Type", "Parent", "Constraints", "Children", "Description"],
            rows,
        )

    def _data_flow(self, package_data: dict) -> str:
        sections = []
        for flow in package_data.get("data_flows", []):
            components = [
                [
                    component.get("name"),
                    component.get("component_type") or "-",
                    component.get("component_class_id") or "-",
                    ", ".join(component.get("connection_references", [])) or "-",
                    str(len(component.get("column_mappings", []))),
                    component.get("description") or "-",
                ]
                for component in flow.get("components", [])
            ]
            sections.append(
                f"### {flow.get('name')}\n\n"
                + self._table(
                    ["Component", "Type", "Class ID", "Connections", "Columns", "Description"],
                    components,
                )
            )

        return "\n\n".join(sections) if sections else "_No data flow metadata detected._"

    def _sql_commands(self, package_data: dict) -> str:
        sections = []
        for index, command in enumerate(package_data.get("sql_commands", []), start=1):
            variables = ", ".join(command.get("referenced_variables", [])) or "-"
            objects = ", ".join(command.get("referenced_objects", [])) or "-"
            dynamic = "Yes" if command.get("is_dynamic") else "No"
            sql = command.get("sql", "").strip()
            sections.append(
                f"### SQL {index}: {command.get('source')}\n\n"
                + self._definition_table(
                    [
                        ("Property", command.get("property")),
                        ("Statement type", command.get("statement_type")),
                        ("Dynamic", dynamic),
                        ("Referenced variables", variables),
                        ("Referenced objects", objects),
                    ]
                )
                + f"\n\n```sql\n{sql}\n```"
            )

        return "\n\n".join(sections) if sections else "_No SQL commands detected._"

    def _business_rules(self, package_data: dict) -> str:
        rules = []
        for command in package_data.get("sql_commands", []):
            objects = ", ".join(command.get("referenced_objects", []))
            if objects:
                rules.append(
                    f"- `{command.get('source')}` references `{objects}` through `{command.get('property')}`."
                )

        return "\n".join(rules) if rules else "_No business rules inferred yet._"

    def _operational_requirements(self, package_data: dict) -> str:
        requirements = [
            "- The package must run with access to all listed connection managers.",
            "- The execution environment must provide all required parameters and variables.",
            "- Generated file paths, local folders, and shared folders must exist before execution.",
            "- Package logging and failure handling must be reviewed against operational standards.",
        ]

        if package_data.get("sql_commands"):
            requirements.append("- Database permissions must allow all extracted SQL operations.")
        if package_data.get("data_flows"):
            requirements.append("- Source and destination schemas must be validated before execution.")

        return "\n".join(requirements)

    def _risks(self, package_data: dict) -> str:
        risks = []

        for command in package_data.get("sql_commands", []):
            if command.get("is_dynamic"):
                risks.append(f"- Dynamic SQL requires implementation review: `{command.get('source')}`.")

        for task in package_data.get("tasks", []):
            task_type = (task.get("task_type") or "").lower()
            if "script" in task_type:
                risks.append(f"- Script task requires manual documentation review: `{task.get('name')}`.")

        for flow in package_data.get("data_flows", []):
            for component in flow.get("components", []):
                component_class = (component.get("component_class_id") or "").lower()
                if "script" in component_class or "custom" in component_class:
                    risks.append(
                        f"- Custom or script data flow component requires manual documentation review: `{component.get('name')}`."
                    )

        return "\n".join(risks) if risks else "_No immediate risks detected from current metadata._"

    def _implementation_backlog(self, package_data: dict) -> str:
        backlog = [
            "Review generated SDD with the package owner.",
            "Confirm source and target datasets for each connection.",
            "Validate inferred business rules against functional knowledge.",
            "Define the functional objective of the package in business terms.",
        ]

        if package_data.get("sql_commands"):
            backlog.append("Review extracted SQL commands and classify implementation impact.")
        if package_data.get("data_flows"):
            backlog.append("Review data flow components, mappings, and transformation rules.")
        if package_data.get("variables") or package_data.get("parameters"):
            backlog.append("Confirm parameter and variable defaults required for execution.")

        for command in package_data.get("sql_commands", []):
            if command.get("is_dynamic"):
                backlog.append(f"Document dynamic SQL resolution for `{command.get('source')}`.")

        for task in package_data.get("tasks", []):
            if task.get("properties", {}).get("is_unknown"):
                backlog.append(f"Classify unknown SSIS task `{task.get('name')}`.")

        return "\n".join(f"- {item}" for item in backlog)

    def _preconditions(self, package_data: dict) -> str:
        items = []
        if package_data.get("connections"):
            items.append("- All configured connection managers are reachable.")
        if package_data.get("parameters"):
            items.append("- Required package parameters are supplied by the caller or environment.")
        if package_data.get("variables"):
            items.append("- Runtime variables are initialized with expected defaults.")

        return "\n".join(items) if items else "_No preconditions inferred from metadata._"

    def _postconditions(self, package_data: dict) -> str:
        items = []
        if package_data.get("data_flows"):
            items.append("- Data flow destinations are populated according to configured mappings.")
        if package_data.get("sql_commands"):
            items.append("- SQL commands complete successfully without unhandled errors.")

        return "\n".join(items) if items else "_No postconditions inferred from metadata._"

    def _connection_location(self, connection: dict) -> str:
        return (
            connection.get("server")
            or connection.get("database")
            or connection.get("file_path")
            or "-"
        )

    def _looks_like_input(self, connection: dict) -> bool:
        connection_type = (connection.get("connection_type") or "").lower()
        return any(
            marker in connection_type
            for marker in ["ole db", "ado.net", "flat file", "excel", "odbc"]
        )

    def _definition_table(self, rows: list[tuple[str, object]]) -> str:
        table_rows = [[label, self._safe_value(value)] for label, value in rows]
        return self._table(["Field", "Value"], table_rows)

    def _table(self, headers: list[str], rows: list[list[object]]) -> str:
        if not rows:
            return "_No data detected._"

        header = "| " + " | ".join(headers) + " |"
        separator = "| " + " | ".join("---" for _ in headers) + " |"
        body = [
            "| " + " | ".join(self._escape_table_cell(value) for value in row) + " |"
            for row in rows
        ]

        return "\n".join([header, separator, *body])

    def _safe_value(self, value: object) -> str:
        if value is None or value == "":
            return "-"

        return str(value)

    def _escape_table_cell(self, value: object) -> str:
        return self._safe_value(value).replace("|", "\\|").replace("\n", "<br>")
