from validator_saas.database import get_session, init_db
from validator_saas.services.validation_service import ValidationService


def setup_module(_: object) -> None:
    init_db()


def test_bacen_validation_detects_issue():
    with get_session() as db:
        service = ValidationService(db)
        org = service.create_organization("Acquirer One", "adquirente", "12.345.678/0001-90")
        regulatory_file = service.register_file(org.id, "bacen", "1.0", "bacen.csv")
        raw_content = "1,12345678000190,C01,abc,20240101,10"  # valor_transacao inválido
        result = service.run_validation(regulatory_file, raw_content)
        assert result.run.status == "completed_with_issues"
        assert any(issue.column_name == "valor_transacao" for issue in result.issues)


def test_dirf_validation_passes():
    with get_session() as db:
        service = ValidationService(db)
        org = service.create_organization("Issuer Two", "emissor", "98.765.432/0001-10")
        regulatory_file = service.register_file(org.id, "dirf", "1.0", "dirf.csv")
        raw_content = "1,12345678000190,,98765432000198,1200.50,150.0,2023"
        result = service.run_validation(regulatory_file, raw_content)
        assert result.run.status == "completed"
        assert not result.issues
