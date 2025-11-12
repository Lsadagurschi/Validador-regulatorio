"""Modelos base representados como dataclasses simples."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Organization:
    id: int
    name: str
    role: str
    tax_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class RegulatoryFile:
    id: int
    organization_id: int
    regulator: str
    layout_version: str
    original_filename: str
    uploaded_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "received"


@dataclass(slots=True)
class ValidationRun:
    id: int
    regulatory_file_id: int
    validator_key: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    status: str = "pending"
    summary: Optional[str] = None


@dataclass(slots=True)
class ValidationIssue:
    id: Optional[int] = None
    validation_run_id: int = 0
    line_number: Optional[int] = None
    column_name: Optional[str] = None
    severity: str = "error"
    message: str = ""


__all__ = [
    "Organization",
    "RegulatoryFile",
    "ValidationRun",
    "ValidationIssue",
]
