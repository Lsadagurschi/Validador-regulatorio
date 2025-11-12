"""Configurações globais da plataforma SaaS."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(slots=True)
class Settings:
    """Representa parâmetros configuráveis do aplicativo."""

    database_url: str = os.getenv("VALIDATOR_DATABASE_URL", "memory://local")
    app_name: str = os.getenv("VALIDATOR_APP_NAME", "Regulatory Validator SaaS")
    api_prefix: str = os.getenv("VALIDATOR_API_PREFIX", "/api")


@lru_cache
def get_settings() -> Settings:
    return Settings()


__all__ = ["Settings", "get_settings"]
