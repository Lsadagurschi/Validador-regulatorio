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


def test_cadoc_3040_validation_passes():
    with get_session() as db:
        service = ValidationService(db)
        org = service.create_organization("Processor Three", "subadquirente", "11.222.333/0001-44")
        regulatory_file = service.register_file(org.id, "cadoc_3040", "1.0", "cadoc3040.csv")
        raw_content = "1,12345678000190,PRD01,100000.50,50000.25,20231231"
        result = service.run_validation(regulatory_file, raw_content)
        assert result.run.status == "completed"
        assert not result.issues


def test_cadoc_3050_validation_detects_invalid_float():
    with get_session() as db:
        service = ValidationService(db)
        org = service.create_organization("Processor Four", "adquirente", "55.666.777/0001-88")
        regulatory_file = service.register_file(org.id, "cadoc_3050", "1.0", "cadoc3050.csv")
        raw_content = "1,12345678000190,MOD01,not-a-number,180,1.5"
        result = service.run_validation(regulatory_file, raw_content)
        assert result.run.status == "completed_with_issues"
        assert any(issue.column_name == "valor_exposicao" for issue in result.issues)


def test_cadoc_6334_validation_accepts_optional_channel():
    with get_session() as db:
        service = ValidationService(db)
        org = service.create_organization("Processor Five", "adquirente", "99.888.777/0001-66")
        regulatory_file = service.register_file(org.id, "cadoc_6334", "1.0", "cadoc6334.csv")
        raw_content = "1,12345678000190,SRV01,120,5000.75,,20240131"
        result = service.run_validation(regulatory_file, raw_content)
        assert result.run.status == "completed"
        assert not result.issues
