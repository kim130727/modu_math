from __future__ import annotations

from dataclasses import dataclass

from modu_math.validators.layout_validator import LayoutValidator
from modu_math.validators.logic_validator import LogicValidator, default_logic_rules
from modu_math.validators.schema_validator import SchemaValidator


@dataclass(slots=True)
class ValidationReport:
    schema_issues: list
    logic_issues: list
    layout_issues: list

    @property
    def ok(self) -> bool:
        all_issues = [*self.schema_issues, *self.logic_issues, *self.layout_issues]
        return all(issue.level != "error" for issue in all_issues)

    def to_text(self) -> str:
        lines: list[str] = ["Validation failed"]
        for section, issues in (
            ("schema", self.schema_issues),
            ("logic", self.logic_issues),
            ("layout", self.layout_issues),
        ):
            if not issues:
                continue
            lines.append(f"[{section}]")
            lines.extend(f"- ({i.level}) {i.code}: {i.message}" for i in issues)
        return "\n".join(lines)


def run_all_validations(semantic: dict) -> ValidationReport:
    schema_issues = SchemaValidator().validate(semantic)
    logic_issues = LogicValidator(default_logic_rules()).validate(semantic)
    layout_issues = LayoutValidator().validate(semantic)
    return ValidationReport(
        schema_issues=schema_issues,
        logic_issues=logic_issues,
        layout_issues=layout_issues,
    )
