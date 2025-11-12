"""Validador para arquivos DIRF."""

from __future__ import annotations

from .base import LayoutValidator
from .layout import FieldDefinition, LayoutDefinition


DIRF_LAYOUT = LayoutDefinition(
    name="DIRF Instituições Financeiras",
    version="1.0",
    fields=(
        FieldDefinition("tipo_registro", int),
        FieldDefinition("cnpj_fonte_pagadora", str, max_length=18),
        FieldDefinition("cpf_beneficiario", str, max_length=14, required=False),
        FieldDefinition("cnpj_beneficiario", str, max_length=18, required=False),
        FieldDefinition("valor_rendimento", float),
        FieldDefinition("imposto_retido", float),
        FieldDefinition("ano_calendario", int),
    ),
)


class DirfValidator(LayoutValidator):
    """Garante aderência ao layout DIRF."""

    key = "dirf"
    regulator = "DIRF"
    layout = DIRF_LAYOUT


__all__ = ["DirfValidator", "DIRF_LAYOUT"]
