import json

from .drug_comparison import SPEC as COMPARE_SPEC, compare_drugs
from .drug_search import SPEC as SEARCH_SPEC, search_drug_info
from .renal_calculator import SPEC as RENAL_SPEC, check_renal_threshold

REGISTRY = {
    "search_drug_info": search_drug_info,
    "compare_drugs": compare_drugs,
    "check_renal_threshold": check_renal_threshold,
}
# (registre central)

TOOL_SPECS = [SEARCH_SPEC, COMPARE_SPEC, RENAL_SPEC]


def _collect_sources(obj, found: set) -> None:
    if isinstance(obj, dict):
        if "source" in obj:
            found.add(str(obj["source"]).split(" ")[0])
        for v in obj.values():
            _collect_sources(v, found)
    elif isinstance(obj, list):
        for v in obj:
            _collect_sources(v, found)


def run_tool(name: str, args: dict) -> tuple[str, list[str]]:
    """Retourne (texte pour le LLM, liste des fichiers sources)."""
    fn = REGISTRY.get(name)
    if not fn:
        return json.dumps({"error": f"unknown tool {name}"}), []
    try:
        result = fn(**args)
    except Exception as e:  # le LLM voit l'erreur et peut corriger son appel
        return json.dumps({"error": str(e)}), []
    sources: set[str] = set()
    _collect_sources(result, sources)
    return json.dumps(result, ensure_ascii=False), sorted(sources)