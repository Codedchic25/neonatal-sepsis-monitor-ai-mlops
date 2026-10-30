"""Clinical access-token hashing and role verification utilities."""

import hashlib
import hmac
import os
import re

_SHA256_HEX_PATTERN = re.compile(r"[0-9a-fA-F]{64}\Z")
_PLACEHOLDER_PREFIXES = ("REPLACE_", "CHANGE_ME", "YOUR_")


class ClinicalAuthService:
    """Verifies clinical access tokens against configured SHA-256 digests."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Return the SHA-256 hexadecimal digest of a string token.

        Note:
            This method is intended for high-entropy access tokens, not
            for storing human passwords.
        """
        if not isinstance(password, str):
            raise TypeError("Access token must be a string.")

        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_role_access(hash_env_var: str, access_token: str) -> bool:
        """Verify a token against a configured SHA-256 digest.

        Missing, malformed, empty, or placeholder configuration fails closed.
        Digest comparison uses a constant-time comparison function.
        """
        if not isinstance(hash_env_var, str):
            return False

        if not isinstance(access_token, str) or not access_token:
            return False

        expected_hash = os.environ.get(hash_env_var, "").strip()

        if not expected_hash:
            return False

        if expected_hash.upper().startswith(_PLACEHOLDER_PREFIXES):
            return False

        if not _SHA256_HEX_PATTERN.fullmatch(expected_hash):
            return False

        supplied_hash = ClinicalAuthService.hash_password(access_token)

        return hmac.compare_digest(
            expected_hash.lower(),
            supplied_hash,
        )
