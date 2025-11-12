"""Validadores para layouts CADOC."""

from __future__ import annotations

from .base import LayoutValidator
from .layout import FieldDefinition, LayoutDefinition


CADOC_3040_LAYOUT = LayoutDefinition(
    name="CADOC 3040",
    version="1.0",
    fields=(
        FieldDefinition("tipo_registro", int),
        FieldDefinition("cnpj_instituicao", str, max_length=18),
        FieldDefinition("codigo_produto", str, max_length=5),
        FieldDefinition("saldo_ativo", float),
        FieldDefinition("saldo_passivo", float),
        FieldDefinition("data_base", str, max_length=8),
    ),
)


CADOC_3050_LAYOUT = LayoutDefinition(
    name="CADOC 3050",
    version="1.0",
    fields=(
        FieldDefinition("tipo_registro", int),
        FieldDefinition("cnpj_instituicao", str, max_length=18),
        FieldDefinition("codigo_modalidade", str, max_length=5),
        FieldDefinition("valor_exposicao", float),
        FieldDefinition("prazo_medio_dias", int),
        FieldDefinition("indice_cobertura", float),
    ),
)


CADOC_6334_LAYOUT = LayoutDefinition(
    name="CADOC 6334",
    version="1.0",
    fields=(
        FieldDefinition("tipo_registro", int),
        FieldDefinition("cnpj_participante", str, max_length=18),
        FieldDefinition("codigo_servico", str, max_length=6),
        FieldDefinition("quantidade_operacoes", int),
        FieldDefinition("valor_total", float),
        FieldDefinition("canal_atendimento", str, max_length=20, required=False),
        FieldDefinition("data_referencia", str, max_length=8),
    ),
)


class Cadoc3040Validator(LayoutValidator):
    """Garante aderência ao layout CADOC 3040."""

    key = "cadoc_3040"
    regulator = "CADOC 3040"
    layout = CADOC_3040_LAYOUT


class Cadoc3050Validator(LayoutValidator):
    """Garante aderência ao layout CADOC 3050."""

    key = "cadoc_3050"
    regulator = "CADOC 3050"
    layout = CADOC_3050_LAYOUT


class Cadoc6334Validator(LayoutValidator):
    """Garante aderência ao layout CADOC 6334."""

    key = "cadoc_6334"
    regulator = "CADOC 6334"
    layout = CADOC_6334_LAYOUT


__all__ = [
    "CADOC_3040_LAYOUT",
    "CADOC_3050_LAYOUT",
    "CADOC_6334_LAYOUT",
    "Cadoc3040Validator",
    "Cadoc3050Validator",
    "Cadoc6334Validator",
]
