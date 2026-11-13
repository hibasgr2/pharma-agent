from ..agent.retriever import get_index


def compare_drugs(drug_a: str, drug_b: str, aspect: str) -> dict:
    idx = get_index()
    return {
        drug_a: idx.search(f"{drug_a} {aspect}", k=4, drug=drug_a),
        drug_b: idx.search(f"{drug_b} {aspect}", k=4, drug=drug_b),
    }


SPEC = {"type": "function", "function": {
    "name": "compare_drugs",
    "description": "Retrieve passages for TWO drugs on the same aspect "
                   "(e.g. contraindications) to compare them side by side.",
    "parameters": {"type": "object", "properties": {
        "drug_a": {"type": "string"}, "drug_b": {"type": "string"},
        "aspect": {"type": "string"}},
        "required": ["drug_a", "drug_b", "aspect"]}}}