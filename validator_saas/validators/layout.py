"""Infraestrutura para definição de layouts regulatórios."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class FieldDefinition:
    """Define propriedades mínimas esperadas em uma coluna."""

    name: str
    type_: Callable[[str], Any]
    required: bool = True
    max_length: int | None = None
    pattern: str | None = None


@dataclass(frozen=True)
class LayoutDefinition:
    """Coleção de campos que descreve um layout regulatório."""

    name: str
    version: str
    fields: tuple[FieldDefinition, ...]
    delimiter: str = ","


def iter_lines(raw_content: str) -> Iterable[tuple[int, list[str]]]:
    """Itera sobre linhas de conteúdo CSV com enumeração de linhas."""

    for line_number, line in enumerate(raw_content.splitlines(), start=1):
        if not line.strip():
            continue
        yield line_number, [value.strip() for value in line.split(",")]


__all__ = ["FieldDefinition", "LayoutDefinition", "iter_lines"]
