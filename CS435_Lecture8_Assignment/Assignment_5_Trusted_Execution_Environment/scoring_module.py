# scoring_module.py
# Rule-based loan scoring logic.
# This file is hashed at startup to simulate TEE code attestation.
# DO NOT modify this file after running generate_config.py without regenerating the config.


def score_applicant(record: dict) -> dict:
    """
    Rule-based loan scoring.

    Args:
        record: dict with keys:
            - credit_score       (int,   300-850)
            - debt_to_income     (float, 0.0-1.0)
            - annual_income      (int,   USD)
            - employment_years   (int,   years at current employer)

    Returns:
        dict with 'score' (0-100) and 'decision' (APPROVED / REVIEW / DENIED)
    """
    score = 0

    # --- Credit Score (max 40 points) ---
    credit = record.get("credit_score", 300)
    if credit >= 750:
        score += 40
    elif credit >= 700:
        score += 30
    elif credit >= 650:
        score += 20
    elif credit >= 600:
        score += 10
    # below 600: 0 points

    # --- Debt-to-Income Ratio (max 30 points) ---
    dti = record.get("debt_to_income", 1.0)
    if dti <= 0.20:
        score += 30
    elif dti <= 0.30:
        score += 25
    elif dti <= 0.40:
        score += 15
    elif dti <= 0.50:
        score += 5
    # above 0.50: 0 points

    # --- Annual Income (max 20 points) ---
    income = record.get("annual_income", 0)
    if income >= 120_000:
        score += 20
    elif income >= 80_000:
        score += 15
    elif income >= 50_000:
        score += 10
    elif income >= 30_000:
        score += 5
    # below 30k: 0 points

    # --- Employment Stability (max 10 points) ---
    emp = record.get("employment_years", 0)
    if emp >= 10:
        score += 10
    elif emp >= 5:
        score += 7
    elif emp >= 2:
        score += 4
    # below 2 years: 0 points

    # --- Decision ---
    if score >= 70:
        decision = "APPROVED"
    elif score >= 45:
        decision = "REVIEW"
    else:
        decision = "DENIED"

    return {"score": score, "decision": decision}
