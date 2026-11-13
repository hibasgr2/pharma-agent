import json
from typing import Any

from langgraph.graph import END, START, StateGraph

from ..config import MAX_STEPS
from ..schemas.models import AgentState
from ..services.llm import chat
from ..tools import TOOL_SPECS, run_tool
from .critic import critic_node
from .planner import planner_node


def agent_node(state: AgentState) -> dict:
    # Au-delà de MAX_STEPS on retire les outils pour forcer une réponse finale
    kwargs = ({"tools": TOOL_SPECS, "tool_choice": "auto"}
              if state["steps"] < MAX_STEPS else {})
    msg = chat(state["messages"], **kwargs).choices[0].message

    entry: dict[str, Any] = {"role": "assistant", "content": msg.content}
    if msg.tool_calls:
        entry["tool_calls"] = [
            {"id": c.id, "type": "function",
             "function": {"name": c.function.name, "arguments": c.function.arguments}}
            for c in msg.tool_calls
        ]
    return {
        "messages": state["messages"] + [entry],
        "steps": state["steps"] + 1,
        "draft": msg.content or state["draft"],
    }


def tools_node(state: AgentState) -> dict:
    messages = list(state["messages"])
    evidence = list(state["evidence"])
    sources = set(state["sources"])
    trace = list(state["trace"])
    for call in messages[-1]["tool_calls"]:
        name = call["function"]["name"]
        args = json.loads(call["function"]["arguments"] or "{}")
        content, srcs = run_tool(name, args)
        sources.update(srcs)
        evidence.append(content)
        trace.append({"tool": name, "args": args})
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": content})
    return {"messages": messages, "evidence": evidence,
            "sources": sorted(sources), "trace": trace}


def route_after_agent(state: AgentState) -> str:
    """Le LLM décide : s'il émet des tool_calls on continue, sinon on passe au critic."""
    return "tools" if state["messages"][-1].get("tool_calls") else "critic"


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("planner", planner_node)
    g.add_node("agent", agent_node)
    g.add_node("tools", tools_node)
    g.add_node("critic", critic_node)

    g.add_edge(START, "planner")
    g.add_edge("planner", "agent")
    g.add_conditional_edges("agent", route_after_agent,
                            {"tools": "tools", "critic": "critic"})
    g.add_edge("tools", "agent")
    g.add_edge("critic", END)
    return g.compile()


GRAPH = build_graph()


def run_agent(question: str) -> dict:
    s = GRAPH.invoke({
        "question": question, "plan": {}, "messages": [], "evidence": [],
        "sources": [], "trace": [], "steps": 0, "draft": "", "review": {}, "answer": "",
    })
    return {
        "answer": s["answer"],
        "sources": s["sources"],
        "plan": s["plan"],
        "tool_calls": s["trace"],
        "review": {"grounded": s["review"].get("grounded"),
                   "issues": s["review"].get("issues", [])},
    }