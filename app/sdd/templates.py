PACKAGE_TEMPLATE = """# SDD: {package_name}

## 1. Specification Metadata

{specification_metadata}

## 2. Package Purpose

{package_purpose}

## 3. Execution Contract

{execution_contract}

## 4. Technical Inventory

### 4.1 Connections

{connections}

### 4.2 Parameters

{parameters}

### 4.3 Variables

{variables}

## 5. Data Contract

### 5.1 Inputs

{inputs}

### 5.2 Outputs

{outputs}

### 5.3 Source To Target Mapping

{source_to_target_mapping}

## 6. Control Flow Specification

{control_flow}

## 7. Data Flow Specification

{data_flow}

## 8. SQL Specification

{sql_commands}

## 9. Business Rules

{business_rules}

## 10. Operational Requirements

{operational_requirements}

## 11. Risks, Gaps, And Open Questions

{risks}

## 12. Implementation Backlog

{implementation_backlog}
"""
