from ..schemas.models import AgentState
from ..services.llm import chat, parse_json
from .prompts import CRITIC_PROMPT, DISCLAIMER


def critic_node(state: AgentState) -> dict:
    evidence = "\n".join(state["evidence"])[:30000]
    review_input = (f"QUESTION:\n{state['question']}\n\n"
                    f"DRAFT:\n{state['draft']}\n\nEVIDENCE:\n{evidence}")
    out = chat([{"role": "system", "content": CRITIC_PROMPT},
                {"role": "user", "content": review_input}])
    review = parse_json(out.choices[0].message.content)
    final = review.get("final_answer") or state["draft"]
    return {"review": review, "answer": f"{final}\n\n{DISCLAIMER}"}