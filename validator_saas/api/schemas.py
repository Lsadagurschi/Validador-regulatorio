"""Esquemas Pydantic utilizados pelas rotas públicas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    name: str = Field(max_length=255)
    role: str = Field(description="Perfil: adquirente | subadquirente | emissor")
    tax_id: str = Field(min_length=14, max_length=18)


class OrganizationRead(BaseModel):
    id: int
    name: str
    role: str
    tax_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ValidationRequest(BaseModel):
    organization_id: int = Field(gt=0)
    regulator: str = Field(description="Orgão regulador alvo: bacen|dimp|dirf")
    layout_version: str = Field(default="1.0")


class ValidationIssueRead(BaseModel):
    line_number: Optional[int] = None
    column_name: Optional[str] = None
    severity: str
    message: str

    model_config = {"from_attributes": True}


class ValidationRunRead(BaseModel):
    id: int
    validator_key: str
    started_at: datetime
    finished_at: Optional[datetime]
    status: str
    summary: Optional[str]
    issues: list[ValidationIssueRead]

    model_config = {"from_attributes": True}


class ValidationResponse(BaseModel):
    validation: ValidationRunRead
    issues: list[ValidationIssueRead]


__all__ = [
    "OrganizationCreate",
    "OrganizationRead",
    "ValidationRequest",
    "ValidationIssueRead",
    "ValidationRunRead",
    "ValidationResponse",
]
