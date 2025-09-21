from langgraph.types import interrupt, Command
from src.agents.state import State
from langchain_core.messages import HumanMessage

def human_node(state: State) -> State:
    if state.get("human") is True:
        print("human")
        task = state.get("results").get(state.get("prev_agent"))[-1]
        edit = interrupt({"AIMessage": task})
        task = f"{task} [Yêu cầu của người dùng] {edit}"
        result = state.get("results").get(state.get("prev_agent"))
        result[-1] = task
        current_results = state.get("results")
        current_results[state.get("prev_agent")] = result
        state.update(results=current_results)
    return state
