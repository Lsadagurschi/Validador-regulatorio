"""Aplicação FastAPI para expor o SaaS."""

from __future__ import annotations

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from ..config import get_settings
from ..database import InMemoryDatabase, get_session, init_db
from ..models import Organization
from ..services.validation_service import ValidationService
from .schemas import OrganizationCreate, OrganizationRead, ValidationRequest, ValidationResponse

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.post("/organizations", response_model=OrganizationRead, status_code=201)
def create_organization(
    payload: OrganizationCreate,
    db: InMemoryDatabase = Depends(get_session),
) -> Organization:
    service = ValidationService(db)
    return service.create_organization(payload.name, payload.role, payload.tax_id)


@app.get("/organizations", response_model=list[OrganizationRead])
def list_organizations(db: InMemoryDatabase = Depends(get_session)) -> list[Organization]:
    service = ValidationService(db)
    return service.list_organizations()


@app.post("/validations", response_model=ValidationResponse)
def validate_file(
    organization_id: int = Form(...),
    regulator: str = Form(...),
    layout_version: str = Form("1.0"),
    file: UploadFile = File(...),
    db: InMemoryDatabase = Depends(get_session),
) -> ValidationResponse:
    payload = ValidationRequest(
        organization_id=organization_id,
        regulator=regulator,
        layout_version=layout_version,
    )
    raw_content = file.file.read().decode("utf-8")
    service = ValidationService(db)
    organization = db.get_organization(payload.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organização não encontrada.")
    regulatory_file = service.register_file(
        organization_id=payload.organization_id,
        regulator=payload.regulator,
        layout_version=payload.layout_version,
        filename=file.filename,
    )
    result = service.run_validation(regulatory_file, raw_content)
    return ValidationResponse(validation=result.run, issues=result.issues)


__all__ = ["app"]
