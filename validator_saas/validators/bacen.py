"""Validador para arquivos de remessa BACEN."""

from __future__ import annotations

from .base import LayoutValidator
from .layout import FieldDefinition, LayoutDefinition


BACEN_LAYOUT = LayoutDefinition(
    name="BACEN 3020",
    version="1.0",
    fields=(
        FieldDefinition("codigo_registro", int),
        FieldDefinition("cnpj_instituicao", str, max_length=18),
        FieldDefinition("tipo_produto", str, max_length=3),
        FieldDefinition("valor_transacao", float),
        FieldDefinition("data_transacao", str, max_length=8),
        FieldDefinition("quantidade_transacoes", int),
    ),
)


class BacenValidator(LayoutValidator):
    """Garante aderência ao layout BACEN."""

    key = "bacen"
    regulator = "BACEN"
    layout = BACEN_LAYOUT


__all__ = ["BacenValidator", "BACEN_LAYOUT"]
