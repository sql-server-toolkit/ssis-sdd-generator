class FabricMigrationAssessment:

    def assess(self, package_data: dict) -> dict:
        blockers = self._blockers(package_data)
        targets = self._target_patterns(package_data)
        component_recommendations = self._component_recommendations(package_data)
        complexity = self._complexity(package_data, blockers)

        return {
            "complexity": complexity,
            "target_patterns": targets,
            "blockers": blockers,
            "component_recommendations": component_recommendations,
            "effort": self._effort(complexity),
            "backlog": self._backlog(package_data, blockers, component_recommendations),
        }

    def _complexity(self, package_data: dict, blockers: list[str]) -> str:
        task_count = len(package_data.get("tasks", []))
        data_flow_count = len(package_data.get("data_flows", []))
        sql_count = len(package_data.get("sql_commands", []))

        score = 0
        score += task_count
        score += data_flow_count * 2
        score += sql_count
        score += len(blockers) * 3

        if score >= 14:
            return "High"
        if score >= 6:
            return "Medium"

        return "Low"

    def _target_patterns(self, package_data: dict) -> list[str]:
        targets = []

        if package_data.get("tasks"):
            targets.append("Data Factory Pipelines")
        if package_data.get("data_flows"):
            targets.extend(["Dataflows Gen2", "Notebooks"])
        if package_data.get("sql_commands"):
            targets.extend(["Warehouse", "Lakehouse"])

        return sorted(set(targets)) or ["Manual review"]

    def _blockers(self, package_data: dict) -> list[str]:
        blockers = []

        for task in package_data.get("tasks", []):
            task_type = (task.get("task_type") or "").lower()
            category = (task.get("properties", {}).get("category") or "").lower()
            if "script" in task_type or "script" in category:
                blockers.append(f"Script task requires manual rewrite: {task.get('name')}")
            if "com" in task_type or "custom" in task_type:
                blockers.append(f"Custom task requires compatibility review: {task.get('name')}")

        for command in package_data.get("sql_commands", []):
            if command.get("is_dynamic"):
                blockers.append(f"Dynamic SQL requires manual validation: {command.get('source')}")

        for connection in package_data.get("connections", []):
            location = connection.get("file_path") or ""
            if "\\\\" in location or location.lower().startswith(("c:\\", "d:\\")):
                blockers.append(f"Local or shared file dependency: {connection.get('name')}")

        for flow in package_data.get("data_flows", []):
            for component in flow.get("components", []):
                component_type = (component.get("component_type") or "").lower()
                component_class = (component.get("component_class_id") or "").lower()
                if "script" in component_type or "custom" in component_class:
                    blockers.append(
                        f"Custom data flow component requires rewrite: {component.get('name')}"
                    )

        return sorted(set(blockers))

    def _component_recommendations(self, package_data: dict) -> list[dict]:
        recommendations = []

        for task in package_data.get("tasks", []):
            category = task.get("properties", {}).get("category")
            if category == "Execute SQL Task":
                target = "Warehouse or Lakehouse SQL activity"
            elif category == "Data Flow Task":
                target = "Dataflows Gen2 or Notebook"
            elif category == "Script Task":
                target = "Notebook or custom activity"
            elif category in {"File System Task", "FTP/SFTP Task"}:
                target = "Data Factory Pipeline copy or storage activity"
            elif category in {"Sequence Container", "Foreach Loop"}:
                target = "Data Factory Pipeline control flow"
            else:
                target = "Manual review"

            recommendations.append(
                {
                    "component": task.get("name"),
                    "source_type": category or task.get("task_type"),
                    "target": target,
                }
            )

        return recommendations

    def _effort(self, complexity: str) -> str:
        if complexity == "High":
            return "High effort; plan a dedicated migration workstream."
        if complexity == "Medium":
            return "Medium effort; validate critical tasks and SQL before implementation."

        return "Low effort; good candidate for an initial migration wave."

    def _backlog(
        self,
        package_data: dict,
        blockers: list[str],
        component_recommendations: list[dict],
    ) -> list[str]:
        backlog = [
            "Review generated SDD with package owner.",
            "Confirm source and target datasets for each connection.",
        ]

        if package_data.get("sql_commands"):
            backlog.append("Validate extracted SQL against Fabric Warehouse or Lakehouse support.")
        if package_data.get("data_flows"):
            backlog.append("Map data flow components to Dataflows Gen2 or Notebook transformations.")

        for blocker in blockers:
            backlog.append(f"Resolve blocker: {blocker}")

        for recommendation in component_recommendations:
            if recommendation.get("target") == "Manual review":
                backlog.append(
                    f"Define migration target for component: {recommendation.get('component')}"
                )

        return backlog
