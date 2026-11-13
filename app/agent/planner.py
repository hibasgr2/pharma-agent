import json

from ..schemas.models import AgentState
from ..services.llm import chat, parse_json
from .prompts import AGENT_PROMPT, PLANNER_PROMPT


def planner_node(state: AgentState) -> dict:
    out = chat([{"role": "system", "content": PLANNER_PROMPT},
                {"role": "user", "content": state["question"]}])
    plan = parse_json(out.choices[0].message.content) or {
        "sub_questions": [state["question"]]
    }
    return {
        "plan": plan,
        "messages": [
            {"role": "system", "content": AGENT_PROMPT.format(plan=json.dumps(plan))},
            {"role": "user", "content": state["question"]},
        ],
    }