"""Camada de aplicação para orquestrar validações."""

from __future__ import annotations

from typing import Any

from ..models import Organization, RegulatoryFile
from ..storage import InMemoryDatabase
from ..validators import VALIDATORS, ValidationResult


class ValidationService:
    """Serviço principal para registro e validação de arquivos regulatórios."""

    def __init__(self, db: InMemoryDatabase) -> None:
        self.db = db

    # Organização -----------------------------------------------------
    def create_organization(self, name: str, role: str, tax_id: str) -> Organization:
        return self.db.create_organization(name=name, role=role, tax_id=tax_id)

    def list_organizations(self) -> list[Organization]:
        return self.db.list_organizations()

    # Upload ----------------------------------------------------------
    def register_file(
        self,
        organization_id: int,
        regulator: str,
        layout_version: str,
        filename: str,
    ) -> RegulatoryFile:
        return self.db.create_file(
            organization_id=organization_id,
            regulator=regulator,
            layout_version=layout_version,
            filename=filename,
        )

    # Validação -------------------------------------------------------
    def run_validation(self, regulatory_file: RegulatoryFile, raw_content: str) -> ValidationResult:
        validator = VALIDATORS.get(regulatory_file.regulator)
        if not validator:
            raise ValueError(f"Validador não encontrado para {regulatory_file.regulator}.")

        run = self.db.create_run(regulatory_file_id=regulatory_file.id, validator_key=validator.key)
        result = validator.validate(raw_content, run)

        for issue in result.issues:
            self.db.add_issue(
                run_id=run.id,
                line_number=issue.line_number,
                column_name=issue.column_name,
                severity=issue.severity,
                message=issue.message,
            )
        regulatory_file.status = result.run.status
        self.db.update_file(regulatory_file)
        self.db.update_run(result.run)
        result.issues = self.db.list_issues_for_run(run.id)
        return result

    # Catálogo de validadores ----------------------------------------
    def list_validators(self) -> list[dict[str, Any]]:
        """Exibe metadados dos validadores registrados."""

        descriptors: list[dict[str, Any]] = []
        for validator in VALIDATORS.values():
            layout = validator.layout
            descriptors.append(
                {
                    "key": validator.key,
                    "regulator": validator.regulator,
                    "layout": {
                        "name": layout.name,
                        "version": layout.version,
                        "fields": [
                            {
                                "name": field.name,
                                "type": getattr(field.type_, "__name__", str(field.type_)),
                                "required": field.required,
                                "max_length": field.max_length,
                            }
                            for field in layout.fields
                        ],
                    },
                }
            )
        return descriptors


__all__ = ["ValidationService"]
