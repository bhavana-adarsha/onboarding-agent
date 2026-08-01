"""Smallest possible LangGraph: two nodes, shared state, no LLM."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question: str
    draft: str
    final: str

def draft_node(state: State) -> dict:
    return {"draft": f"Draft answer to: {state['question']}"}

def polish_node(state: State) -> dict:
    return {"final": state["draft"].replace("Draft", "Polished")}

builder = StateGraph(State)
builder.add_node("draft", draft_node)
builder.add_node("polish", polish_node)
builder.add_edge(START, "draft")
builder.add_edge("draft", "polish")
builder.add_edge("polish", END)
graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"question": "how does PTO work?"})
    print(result)