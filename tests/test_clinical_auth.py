"""Tests for clinical access-token hashing and SHA-256 role verification."""

import hashlib
import os
import re
import sys
from unittest import mock

import pytest

# Ensure the project root is available when running tests directly.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.services.auth_service import ClinicalAuthService


def test_hash_password_returns_consistent_sha256_digest() -> None:
    """Verify deterministic output and the SHA-256 hexadecimal format."""
    token = "temporary_test_access_token"

    digest_1 = ClinicalAuthService.hash_password(token)
    digest_2 = ClinicalAuthService.hash_password(token)

    assert digest_1 == digest_2
    assert re.fullmatch(r"[0-9a-f]{64}", digest_1)


def test_hash_password_rejects_non_string_input() -> None:
    """Reject values that are not strings by raising a TypeError."""
    with pytest.raises(TypeError, match="Access token must be a string."):
        ClinicalAuthService.hash_password(123)  # type: ignore[arg-type]


def test_verify_role_access_missing_environment_variable() -> None:
    """Reject a role whose environment variable is absent."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert (
            ClinicalAuthService.verify_role_access(
                "NON_EXISTENT_ROLE_HASH",
                "temporary_token",
            )
            is False
        )


def test_verify_role_access_accepts_matching_digest() -> None:
    """Accept a token when its computed digest matches the configured digest."""
    token = "temporary_clinical_access_token"
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()

    with mock.patch.dict(os.environ, {"TEST_ROLE_HASH": digest}):
        assert ClinicalAuthService.verify_role_access("TEST_ROLE_HASH", token)


def test_verify_role_access_rejects_wrong_token() -> None:
    """Reject a token that does not match the configured digest."""
    token = "temporary_clinical_access_token"
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()

    with mock.patch.dict(os.environ, {"TEST_ROLE_HASH": digest}):
        assert not ClinicalAuthService.verify_role_access(
            "TEST_ROLE_HASH",
            "different_temporary_token",
        )


def test_verify_role_access_rejects_empty_token() -> None:
    """Reject an empty access token."""
    digest = hashlib.sha256(b"temporary_token").hexdigest()

    with mock.patch.dict(os.environ, {"TEST_ROLE_HASH": digest}):
        assert not ClinicalAuthService.verify_role_access("TEST_ROLE_HASH", "")


def test_verify_role_access_rejects_malformed_digest() -> None:
    """Reject a digest that is not 64 hexadecimal characters."""
    with mock.patch.dict(os.environ, {"TEST_ROLE_HASH": "invalid_digest"}):
        assert not ClinicalAuthService.verify_role_access(
            "TEST_ROLE_HASH",
            "temporary_token",
        )


def test_verify_role_access_rejects_placeholder() -> None:
    """Reject example-template placeholders."""
    with mock.patch.dict(
        os.environ,
        {"TEST_ROLE_HASH": "REPLACE_WITH_SHA256_HEX_DIGEST"},
    ):
        assert not ClinicalAuthService.verify_role_access(
            "TEST_ROLE_HASH",
            "temporary_token",
        )


def test_verify_role_access_rejects_non_string_arguments() -> None:
    """Reject invalid argument types without raising."""
    assert not ClinicalAuthService.verify_role_access(
        None,  # type: ignore[arg-type]
        "temporary_token",
    )
    assert not ClinicalAuthService.verify_role_access(
        "TEST_ROLE_HASH",
        None,  # type: ignore[arg-type]
    )
