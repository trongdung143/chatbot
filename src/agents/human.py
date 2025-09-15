from langgraph.types import interrupt, Command
from src.agents.state import State
from langchain_core.messages import HumanMessage


def human_node(state: State) -> State:
    if state["human"]:
        edit = interrupt({"AIMessage": state["task"]})
        state["messages"].append(HumanMessage(content=f"{state["task"]}\n{edit}"))
        state["human"] = False
    return state
