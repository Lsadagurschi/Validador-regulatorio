"""Base abstrata para validadores regulatórios."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from ..models import ValidationIssue, ValidationRun
from .layout import FieldDefinition, LayoutDefinition, iter_lines


@dataclass
class ValidationResult:
    """Representa o resultado de uma validação."""

    run: ValidationRun
    issues: list[ValidationIssue]


class Validator(Protocol):
    """Assinatura esperada para validadores concretos."""

    key: str

    def validate(self, raw_content: str, run: ValidationRun) -> ValidationResult:  # pragma: no cover - interface
        ...


class LayoutValidator:
    """Implementação genérica baseada em layouts declarativos."""

    key: str
    regulator: str
    layout: LayoutDefinition

    def _parse_value(self, value: str, field: FieldDefinition) -> str | None:
        """Garante o tipo e comprimento de uma coluna."""

        if field.max_length and len(value) > field.max_length:
            return f"Tamanho máximo excedido ({len(value)}/{field.max_length})."
        try:
            field.type_(value)
        except Exception as exc:  # noqa: BLE001 - queremos mensagem raiz
            return f"Valor inválido ({exc})."
        return None

    def validate(self, raw_content: str, run: ValidationRun) -> ValidationResult:
        issues: list[ValidationIssue] = []
        header = [field.name for field in self.layout.fields]
        for line_number, values in iter_lines(raw_content):
            if len(values) != len(header):
                issues.append(
                    ValidationIssue(
                        validation_run_id=run.id,
                        line_number=line_number,
                        severity="error",
                        message=f"Quantidade de colunas incorreta: esperado {len(header)}, recebido {len(values)}.",
                    )
                )
                continue
            for value, field in zip(values, self.layout.fields, strict=True):
                if not value and field.required:
                    issues.append(
                        ValidationIssue(
                            validation_run_id=run.id,
                            line_number=line_number,
                            column_name=field.name,
                            severity="error",
                            message="Campo obrigatório ausente.",
                        )
                    )
                    continue
                if not value and not field.required:
                    continue
                problem = self._parse_value(value, field)
                if problem:
                    issues.append(
                        ValidationIssue(
                            validation_run_id=run.id,
                            line_number=line_number,
                            column_name=field.name,
                            severity="error",
                            message=problem,
                        )
                    )
        run.finished_at = datetime.utcnow()
        run.status = "completed" if not issues else "completed_with_issues"
        run.summary = (
            "Arquivo validado sem inconsistências."
            if not issues
            else f"Foram encontradas {len(issues)} inconsistências."
        )
        return ValidationResult(run=run, issues=issues)


__all__ = [
    "LayoutValidator",
    "Validator",
    "ValidationResult",
]
