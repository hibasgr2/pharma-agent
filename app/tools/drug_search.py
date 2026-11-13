from ..agent.retriever import get_index


def search_drug_info(query: str, drug: str | None = None, k: int = 5) -> list[dict]:
    return get_index().search(query, k=k, drug=drug)


SPEC = {"type": "function", "function": {
    "name": "search_drug_info",
    "description": "Semantic search in the drug label corpus. Use for any "
                   "question about one drug (contraindications, dosage, "
                   "interactions, warnings...).",
    "parameters": {"type": "object", "properties": {
        "query": {"type": "string"},
        "drug": {"type": "string",
                 "description": "Optional drug name to restrict the search, e.g. 'warfarin'"},
        "k": {"type": "integer", "default": 5}},
        "required": ["query"]}}}