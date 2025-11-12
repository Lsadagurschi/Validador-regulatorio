"""Validador para arquivos DIMP (TED/TEF)."""

from __future__ import annotations

from .base import LayoutValidator
from .layout import FieldDefinition, LayoutDefinition


DIMP_LAYOUT = LayoutDefinition(
    name="DIMP TED/TEF",
    version="1.0",
    fields=(
        FieldDefinition("codigo_registro", int),
        FieldDefinition("cnpj_participante", str, max_length=18),
        FieldDefinition("modalidade", str, max_length=4),
        FieldDefinition("valor_total", float),
        FieldDefinition("quantidade_operacoes", int),
        FieldDefinition("data_referencia", str, max_length=8),
    ),
)


class DimpValidator(LayoutValidator):
    """Garante aderência às instruções do DIMP."""

    key = "dimp"
    regulator = "DIMP"
    layout = DIMP_LAYOUT


__all__ = ["DimpValidator", "DIMP_LAYOUT"]
