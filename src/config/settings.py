"""Centralized application configuration and environment settings."""

import os
import re
from typing import Final

from dotenv import load_dotenv

_SHA256_HEX_PATTERN = re.compile(r"[0-9a-fA-F]{64}\Z")
_PLACEHOLDER_PREFIXES = ("REPLACE_", "CHANGE_ME", "YOUR_")


def _read_optional_value(name: str) -> str | None:
    """Return a non-empty environment variable, or None if unavailable."""
    value = os.getenv(name, "").strip()
    return value or None


def _read_sha256_digest(name: str) -> str | None:
    """Return a valid configured SHA-256 digest, or None if invalid."""
    value = _read_optional_value(name)

    if value is None:
        return None

    if value.upper().startswith(_PLACEHOLDER_PREFIXES):
        return None

    if not _SHA256_HEX_PATTERN.fullmatch(value):
        return None

    return value.lower()


# Load the project environment file when present. Existing environment
# variables take precedence over values from .env.
load_dotenv(override=False)


class AppSettings:
    """Expose validated application configuration values."""

    # Runtime configuration
    APP_ENV: Final[str] = os.getenv("APP_ENV", "development").strip()
    DEBUG: Final[bool] = os.getenv("DEBUG", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO").strip().upper()

    # Application secret
    SECRET_KEY: Final[str | None] = _read_optional_value("SECRET_KEY")

    # Clinical role authentication digests
    SEF_SECTIE_HASH: Final[str | None] = _read_sha256_digest("SEF_SECTIE_HASH")
    MEDIC_ECHIPA_HASH: Final[str | None] = _read_sha256_digest("MEDIC_ECHIPA_HASH")
    MEDIC_GARDA_HASH: Final[str | None] = _read_sha256_digest("MEDIC_GARDA_HASH")
    REZIDENT_HASH: Final[str | None] = _read_sha256_digest("REZIDENT_HASH")
    ASISTENT_HASH: Final[str | None] = _read_sha256_digest("ASISTENT_HASH")

    # External integrations
    GROQ_API_KEY: Final[str | None] = _read_optional_value("GROQ_API_KEY")

    # Persistent storage and model routing
    DATABASE_URL: Final[str] = os.getenv(
        "DATABASE_URL",
        "sqlite:///sepsis_neonatal.db",
    ).strip()
    MODEL_CORE: Final[str] = os.getenv(
        "GROQ_MODEL_NAME",
        "llama-3.1-8b-instant",
    ).strip()
    TEMPERATURE: Final[float] = 0.1
    MAX_TOKENS: Final[int] = 1024
