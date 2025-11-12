from validator_saas.database import get_session, init_db
from validator_saas.services.validation_service import ValidationService


def setup_module(_: object) -> None:
    init_db()


def test_list_validators_exposes_layout_metadata():
    with get_session() as db:
        service = ValidationService(db)
        catalog = service.list_validators()
    keys = {item["key"] for item in catalog}
    assert {"bacen", "dimp", "dirf", "cadoc_3040", "cadoc_3050", "cadoc_6334"}.issubset(keys)
    for item in catalog:
        layout = item["layout"]
        assert "name" in layout and "version" in layout
        assert isinstance(layout["fields"], list)
        assert all("name" in field and "type" in field for field in layout["fields"])
