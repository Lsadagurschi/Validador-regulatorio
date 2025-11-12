"""Compat layer para reutilizar a infraestrutura de armazenamento."""

from __future__ import annotations

from .storage import InMemoryDatabase, get_session, init_db

__all__ = ["InMemoryDatabase", "get_session", "init_db"]
