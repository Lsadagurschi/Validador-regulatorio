"""Coleção de validadores disponíveis."""

from .bacen import BacenValidator
from .dimp import DimpValidator
from .dirf import DirfValidator
from .base import LayoutValidator, ValidationResult, Validator

VALIDATORS = {
    BacenValidator.key: BacenValidator(),
    DimpValidator.key: DimpValidator(),
    DirfValidator.key: DirfValidator(),
}

__all__ = [
    "BacenValidator",
    "DimpValidator",
    "DirfValidator",
    "LayoutValidator",
    "ValidationResult",
    "Validator",
    "VALIDATORS",
]
