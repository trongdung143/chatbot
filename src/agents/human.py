from langgraph.types import interrupt, Command
from src.agents.state import State
from langchain_core.messages import HumanMessage


def human_node(state: State) -> State:
    print("human_node")
    if state.get("human") is True:
        edit = interrupt({"AIMessage": state.get("result").content})
        state.update(messages=[HumanMessage(content=f"{state.get("task")}\n{edit}")])
        state["human"] = False
    return state
