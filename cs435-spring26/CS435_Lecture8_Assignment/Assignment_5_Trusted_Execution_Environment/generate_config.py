# generate_config.py
# One-time setup script.
# Computes the SHA-256 hash of scoring_module.py and saves it to config.json.
#
# Run this ONCE before running run_normal.py or run_tampered.py.
# Re-run it if you intentionally update scoring_module.py to regenerate a valid hash.

import hashlib
import json
import sys
from pathlib import Path

MODULE_PATH = "scoring_module.py"
CONFIG_PATH = "config.json"


def compute_hash(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


if __name__ == "__main__":
    if not Path(MODULE_PATH).exists():
        print(f"[ERROR] {MODULE_PATH} not found. Make sure you run this from the project directory.")
        sys.exit(1)

    module_hash = compute_hash(MODULE_PATH)

    config = {"expected_module_hash": module_hash}
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print(f"[CONFIG] Hashed: {MODULE_PATH}")
    print(f"[CONFIG] SHA-256: {module_hash}")
    print(f"[CONFIG] Saved expected hash to {CONFIG_PATH}")
    print(f"\n[READY] You can now run run_normal.py and run_tampered.py")
