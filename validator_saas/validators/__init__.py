"""Coleção de validadores disponíveis."""

from .bacen import BacenValidator
from .cadoc import Cadoc3040Validator, Cadoc3050Validator, Cadoc6334Validator
from .dimp import DimpValidator
from .dirf import DirfValidator
from .base import LayoutValidator, ValidationResult, Validator

VALIDATORS = {
    BacenValidator.key: BacenValidator(),
    Cadoc3040Validator.key: Cadoc3040Validator(),
    Cadoc3050Validator.key: Cadoc3050Validator(),
    Cadoc6334Validator.key: Cadoc6334Validator(),
    DimpValidator.key: DimpValidator(),
    DirfValidator.key: DirfValidator(),
}

__all__ = [
    "BacenValidator",
    "Cadoc3040Validator",
    "Cadoc3050Validator",
    "Cadoc6334Validator",
    "DimpValidator",
    "DirfValidator",
    "LayoutValidator",
    "ValidationResult",
    "Validator",
    "VALIDATORS",
]
