"""Armazenamento em memória para prototipagem da plataforma."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from itertools import count
from typing import Dict

from .models import Organization, RegulatoryFile, ValidationIssue, ValidationRun


class InMemoryDatabase:
    """Simula persistência de dados para fins de prototipagem."""

    def __init__(self) -> None:
        self._organization_seq = count(1)
        self._file_seq = count(1)
        self._run_seq = count(1)
        self._issue_seq = count(1)
        self.organizations: Dict[int, Organization] = {}
        self.files: Dict[int, RegulatoryFile] = {}
        self.validation_runs: Dict[int, ValidationRun] = {}
        self.issues: Dict[int, ValidationIssue] = {}

    # Organizações --------------------------------------------------
    def create_organization(self, name: str, role: str, tax_id: str) -> Organization:
        organization = Organization(id=next(self._organization_seq), name=name, role=role, tax_id=tax_id)
        self.organizations[organization.id] = organization
        return organization

    def list_organizations(self) -> list[Organization]:
        return sorted(self.organizations.values(), key=lambda org: org.created_at)

    def get_organization(self, organization_id: int) -> Organization | None:
        return self.organizations.get(organization_id)

    # Arquivos -------------------------------------------------------
    def create_file(
        self,
        organization_id: int,
        regulator: str,
        layout_version: str,
        filename: str,
    ) -> RegulatoryFile:
        regulatory_file = RegulatoryFile(
            id=next(self._file_seq),
            organization_id=organization_id,
            regulator=regulator,
            layout_version=layout_version,
            original_filename=filename,
        )
        self.files[regulatory_file.id] = regulatory_file
        return regulatory_file

    def update_file(self, regulatory_file: RegulatoryFile) -> None:
        self.files[regulatory_file.id] = regulatory_file

    # Execuções ------------------------------------------------------
    def create_run(self, regulatory_file_id: int, validator_key: str) -> ValidationRun:
        run = ValidationRun(
            id=next(self._run_seq),
            regulatory_file_id=regulatory_file_id,
            validator_key=validator_key,
            started_at=datetime.utcnow(),
            status="running",
        )
        self.validation_runs[run.id] = run
        return run

    def update_run(self, run: ValidationRun) -> None:
        self.validation_runs[run.id] = run

    def list_issues_for_run(self, run_id: int) -> list[ValidationIssue]:
        return [issue for issue in self.issues.values() if issue.validation_run_id == run_id]

    def add_issue(
        self,
        run_id: int,
        line_number: int | None,
        column_name: str | None,
        severity: str,
        message: str,
    ) -> ValidationIssue:
        issue = ValidationIssue(
            id=next(self._issue_seq),
            validation_run_id=run_id,
            line_number=line_number,
            column_name=column_name,
            severity=severity,
            message=message,
        )
        self.issues[issue.id] = issue
        return issue


_db = InMemoryDatabase()


def init_db() -> None:  # pragma: no cover - nada a inicializar
    """Mantido para compatibilidade com a API FastAPI."""


@contextmanager
def get_session() -> Iterator[InMemoryDatabase]:
    """Fornece a instância singleton do banco de dados."""

    yield _db


__all__ = ["InMemoryDatabase", "get_session", "init_db"]
