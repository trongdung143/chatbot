from langgraph.types import interrupt, Command
from src.agents.state import State
from langchain_core.messages import HumanMessage


def human_node(state: State) -> State:
    if state.get("human") is True:
        print("human")
        edit = interrupt({"AIMessage": state.get("result").content})
        state.update(result=HumanMessage(content=edit))
    return state
