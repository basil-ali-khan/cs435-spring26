# run_normal.py
# TEE-Style Loan Scoring Demo — NORMAL (attested) run.
#
# Demonstrates that the protected service:
#   1. Verifies the scoring module hash (attestation passes).
#   2. Decrypts the applicant payload only after verification.
#   3. Returns scores and decisions without leaking raw applicant data.
#
# NOTE: This is a SOFTWARE SIMULATION of a TEE workflow.
#       It does NOT use real hardware (SGX, AMD SEV, AWS Nitro, etc.).

import json

from cryptography.fernet import Fernet

from tee_service import protected_service

# ---------------------------------------------------------------------------
# Synthetic applicant dataset (clearly labelled — no real data)
# ---------------------------------------------------------------------------
SYNTHETIC_APPLICANTS = [
    {
        "applicant_id": "SYNTH-001",
        "credit_score": 720,
        "debt_to_income": 0.32,
        "annual_income": 85_000,
        "employment_years": 6,
    },
    {
        "applicant_id": "SYNTH-002",
        "credit_score": 580,
        "debt_to_income": 0.55,
        "annual_income": 35_000,
        "employment_years": 1,
    },
    {
        "applicant_id": "SYNTH-003",
        "credit_score": 800,
        "debt_to_income": 0.18,
        "annual_income": 130_000,
        "employment_years": 12,
    },
    {
        "applicant_id": "SYNTH-004",
        "credit_score": 650,
        "debt_to_income": 0.42,
        "annual_income": 55_000,
        "employment_years": 3,
    },
]


def encrypt_payload(record: dict, key: bytes) -> bytes:
    """Encrypt a JSON applicant record with Fernet symmetric encryption."""
    f = Fernet(key)
    return f.encrypt(json.dumps(record).encode())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 65)
    print("  TEE-STYLE LOAN SCORING — NORMAL RUN  (SOFTWARE SIMULATION)")
    print("=" * 65)
    print("[NOTICE] This simulates a TEE attestation workflow in software.")
    print("         In production, use AWS Nitro Enclaves, Azure Confidential")
    print("         VMs, or GCP Confidential VMs for hardware-level isolation.\n")

    # Generate a fresh symmetric key.
    # In a real TEE deployment, this key would be provisioned by a key-management
    # service only after hardware attestation succeeds.
    key = Fernet.generate_key()
    print("[ENCLAVE] Symmetric key generated (not printed for security).\n")

    results = []

    for applicant in SYNTHETIC_APPLICANTS:
        encrypted = encrypt_payload(applicant, key)
        print(f"[CLIENT]  Encrypting and sending payload for {applicant['applicant_id']}...")

        result = protected_service(encrypted, key)
        results.append(result)

        if result["status"] == "SUCCESS":
            print(f"[ENCLAVE] Attestation passed  — hash matches expected.")
            print(f"[RESULT]  {result['applicant_id']} → score={result['score']:3d}  decision={result['decision']}")
        elif result["status"] == "BLOCKED":
            print(f"[ENCLAVE] BLOCKED — {result['reason']}")
        else:
            print(f"[ENCLAVE] ERROR   — {result.get('reason', 'unknown error')}")
        print()

    # Summary
    print("=" * 65)
    print("  SUMMARY")
    print("=" * 65)
    approved = [r for r in results if r.get("decision") == "APPROVED"]
    review   = [r for r in results if r.get("decision") == "REVIEW"]
    denied   = [r for r in results if r.get("decision") == "DENIED"]
    blocked  = [r for r in results if r.get("status") == "BLOCKED"]

    for r in results:
        if r["status"] == "SUCCESS":
            tag = f"score={r['score']:3d}  {r['decision']}"
        else:
            tag = r["status"]
        print(f"  {r.get('applicant_id', '?'):12s}  {tag}")

    print()
    print(f"  Approved: {len(approved)}  |  Review: {len(review)}  |  Denied: {len(denied)}  |  Blocked: {len(blocked)}")
    print()
    print("[SECURITY] Raw applicant records were never printed or logged.")
    print("[DONE]     Normal run complete.")
