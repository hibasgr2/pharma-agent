# Règles déterministes extraites du label DailyMed (metformin, sections 2.3 / 4 / 5.1)
RENAL_RULES = {
    "metformin": {
        "source": "dailymed-metformin.md (sections 2.3, 4, 5.1)",
        "rules": [
            (30, "contraindicated", "eGFR below 30: contraindicated"),
            (45, "initiation_not_recommended",
             "eGFR 30-45: initiation not recommended; if already on it and eGFR "
             "falls below 45, assess benefit/risk of continuing"),
        ],
    }
}


def check_renal_threshold(drug: str, egfr: float) -> dict:
    rule = RENAL_RULES.get(drug.lower())
    if not rule:
        return {"error": f"No numeric rule for '{drug}'. Use search_drug_info instead."}
    for limit, status, message in rule["rules"]:
        if egfr < limit:
            return {"drug": drug, "egfr": egfr, "status": status,
                    "message": message, "source": rule["source"]}
    return {"drug": drug, "egfr": egfr,
            "status": "no_renal_restriction_at_this_level",
            "message": "eGFR >= 45: no renal contraindication in the label",
            "source": rule["source"]}


SPEC = {"type": "function", "function": {
    "name": "check_renal_threshold",
    "description": "Check a patient's eGFR (mL/min/1.73m2) against the label's "
                   "renal thresholds for a drug (currently metformin).",
    "parameters": {"type": "object", "properties": {
        "drug": {"type": "string"}, "egfr": {"type": "number"}},
        "required": ["drug", "egfr"]}}}