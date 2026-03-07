# run_tampered.py
# TEE-Style Loan Scoring Demo — TAMPERED (blocked) run.
#
# Simulates an attacker modifying scoring_module.py after the expected hash
# was recorded. Demonstrates that the protected service detects the change
# and refuses to decrypt or score.
#
# What this script does:
#   1. Saves the original scoring_module.py to a backup.
#   2. Overwrites scoring_module.py with malicious logic.
#   3. Calls protected_service() — which should BLOCK execution.
#   4. Restores scoring_module.py from the backup (always, even on error).
#
# NOTE: This is a SOFTWARE SIMULATION of a TEE workflow.
#       It does NOT use real hardware (SGX, AMD SEV, AWS Nitro, etc.).

import json
import os
import shutil

from cryptography.fernet import Fernet

from tee_service import protected_service

# ---------------------------------------------------------------------------
# Synthetic applicant (clearly labelled — no real data)
# ---------------------------------------------------------------------------
SYNTHETIC_APPLICANT = {
    "applicant_id": "SYNTH-TAMPER-001",
    "credit_score": 560,
    "debt_to_income": 0.48,
    "annual_income": 40_000,
    "employment_years": 1,
}

# ---------------------------------------------------------------------------
# The malicious replacement for scoring_module.py
# An attacker might inject this to bypass real scoring and always approve.
# ---------------------------------------------------------------------------
TAMPERED_CODE = '''\
# scoring_module.py — TAMPERED BY ATTACKER (demo only)
# This version bypasses all scoring logic and unconditionally approves every application.

def score_applicant(record: dict) -> dict:
    # Malicious override: always return maximum score to approve all applicants.
    return {"score": 100, "decision": "APPROVED"}
'''

MODULE_PATH = "scoring_module.py"
BACKUP_PATH = "scoring_module.py.bak"


def encrypt_payload(record: dict, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(json.dumps(record).encode())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 65)
    print("  TEE-STYLE LOAN SCORING — TAMPERED RUN  (SOFTWARE SIMULATION)")
    print("=" * 65)
    print("[NOTICE] This simulates an attacker tampering with the scoring module")
    print("         after the expected hash was registered in config.json.\n")

    key = Fernet.generate_key()
    encrypted = encrypt_payload(SYNTHETIC_APPLICANT, key)

    print(f"[CLIENT]  Encrypted payload prepared for {SYNTHETIC_APPLICANT['applicant_id']}.")
    print()

    # ── Tamper step ───────────────────────────────────────────────────────────
    print("[ATTACKER] Backing up original scoring_module.py...")
    shutil.copy(MODULE_PATH, BACKUP_PATH)

    print("[ATTACKER] Overwriting scoring_module.py with malicious logic...")
    with open(MODULE_PATH, "w") as f:
        f.write(TAMPERED_CODE)
    print("[ATTACKER] scoring_module.py has been tampered.\n")

    # ── Attempt to call protected service ────────────────────────────────────
    try:
        print(f"[CLIENT]  Sending encrypted payload to protected_service()...")
        result = protected_service(encrypted, key)
        print()

        if result["status"] == "BLOCKED":
            print("[ENCLAVE] *** ATTESTATION FAILED — EXECUTION BLOCKED ***")
            print(f"[ENCLAVE] Reason          : {result['reason']}")
            print(f"[ENCLAVE] Expected hash   : {result['expected_hash_prefix']}")
            print(f"[ENCLAVE] Actual hash     : {result['actual_hash_prefix']}")
            print()
            print("[SECURITY] The payload was NOT decrypted.")
            print("[SECURITY] Applicant data remains fully protected.")
        elif result["status"] == "SUCCESS":
            # This should never happen in a correct simulation
            print("[WARNING]  Service returned SUCCESS despite tampered code.")
            print("           Check that generate_config.py was run before tampering.")
        else:
            print(f"[ENCLAVE] ERROR: {result.get('reason', 'unknown')}")

    finally:
        # ── Always restore the original module ───────────────────────────────
        shutil.copy(BACKUP_PATH, MODULE_PATH)
        os.remove(BACKUP_PATH)
        print()
        print("[DEMO]    scoring_module.py restored to original.")
        print("[DONE]    Tampered run complete.")
