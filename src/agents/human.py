from langgraph.types import interrupt, Command
from src.agents.state import State


def human_node(state: State) -> State:
    if state["human"]:
        interrupt({"AIMessage": state["task"]})
    else:
        return state
