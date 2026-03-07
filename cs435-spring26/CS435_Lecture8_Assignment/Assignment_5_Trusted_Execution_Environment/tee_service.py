# tee_service.py
# TEE-style protected scoring service (SOFTWARE SIMULATION — not real SGX/AMD SEV/Nitro).
#
# Design:
#   1. Measurement  — compute SHA-256 of scoring_module.py (simulates enclave measurement)
#   2. Attestation  — compare measurement against expected hash from config.json
#   3. Decrypt      — only if attestation passes, decrypt the encrypted applicant payload
#   4. Score        — run scoring_module.score_applicant() and return minimal result
#   5. Safe output  — raw applicant fields are NEVER returned or logged

import hashlib
import importlib
import json
import sys
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _compute_file_hash(filepath: str) -> str:
    """Return the SHA-256 hex digest of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _load_expected_hash(config_path: str = "config.json") -> str:
    """Load the expected module hash from the config file."""
    with open(config_path, "r") as f:
        config = json.load(f)
    return config["expected_module_hash"]


# ---------------------------------------------------------------------------
# Protected service entry point
# ---------------------------------------------------------------------------

def protected_service(
    encrypted_payload: bytes,
    fernet_key: bytes,
    module_path: str = "scoring_module.py",
    config_path: str = "config.json",
) -> dict:
    """
    TEE-style protected service.

    Steps
    -----
    1. Compute SHA-256 of `module_path` (attestation / measurement).
    2. Compare against the expected hash in `config_path`.
    3. If mismatch  → return BLOCKED result immediately (no decryption).
    4. If match     → decrypt payload with `fernet_key`, invoke score_applicant(),
                      and return only the score + decision (no raw fields).

    Parameters
    ----------
    encrypted_payload : bytes
        Fernet-encrypted JSON blob of the applicant record.
    fernet_key : bytes
        The symmetric key used to encrypt the payload.
    module_path : str
        Path to the scoring module file to measure.
    config_path : str
        Path to the JSON config holding the expected hash.

    Returns
    -------
    dict with keys: status, and either (applicant_id, score, decision) or (reason, ...).
    """

    # ── Step 1 & 2: Attestation check ────────────────────────────────────────
    try:
        actual_hash = _compute_file_hash(module_path)
        expected_hash = _load_expected_hash(config_path)
    except FileNotFoundError as e:
        return {
            "status": "ERROR",
            "reason": f"Could not perform attestation: {e}",
        }

    if actual_hash != expected_hash:
        # Intentionally reveal only a prefix of each hash for diagnostics
        return {
            "status": "BLOCKED",
            "reason": "Code measurement mismatch — attestation failed. Payload was NOT decrypted.",
            "expected_hash_prefix": expected_hash[:24] + "...",
            "actual_hash_prefix":   actual_hash[:24]   + "...",
        }

    # ── Step 3: Decrypt applicant payload (only reached after verification) ──
    try:
        f = Fernet(fernet_key)
        decrypted_bytes = f.decrypt(encrypted_payload)
        record = json.loads(decrypted_bytes.decode())
    except InvalidToken:
        return {"status": "ERROR", "reason": "Decryption failed — invalid key or corrupted payload."}
    except json.JSONDecodeError:
        return {"status": "ERROR", "reason": "Payload is not valid JSON after decryption."}

    # ── Step 4: Run scoring logic ─────────────────────────────────────────────
    # Reload module so any on-disk changes (including tampering) are reflected.
    if "scoring_module" in sys.modules:
        scoring_module = importlib.reload(sys.modules["scoring_module"])
    else:
        scoring_module = importlib.import_module("scoring_module")

    result = scoring_module.score_applicant(record)

    # ── Step 5: Return minimal result — no raw applicant data ────────────────
    return {
        "status": "SUCCESS",
        "applicant_id": record.get("applicant_id", "UNKNOWN"),
        "score": result["score"],
        "decision": result["decision"],
    }
