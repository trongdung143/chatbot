from typing import Sequence
from langchain_core.tools.base import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.setup import GOOGLE_API_KEY
from src.agents.state import State
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


class BaseAgent:
    def __init__(
        self,
        agent_name: str,
        tools: Sequence[BaseTool] | None = None,
        model: object | None = None,
    ) -> None:
        self._tools = list(tools or [])
        self._agent_name = agent_name

        self._model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GOOGLE_API_KEY,
            disable_streaming=False,
        ).bind_tools(self._tools)

    async def process(self, state: State) -> State:
        return state

    def get_builder(self) -> StateGraph:
        graph = StateGraph(State)
        graph.add_node(self._agent_name, self.process)

        if self._tools:
            graph.add_node("tools", ToolNode(self._tools))
            graph.add_conditional_edges(self._agent_name, tools_condition)
            graph.add_edge("tools", self._agent_name)
        else:
            pass

        graph.set_entry_point(self._agent_name)
        return graph

    def log_run(self, state: State, task: str, result: str, start: float, end: float):
        state["agent_logs"].append(
            {
                "agent_name": self._agent_name,
                "task": task,
                "result": result,
                "step": len(state["agent_logs"]) + 1,
                "start_time": start,
                "end_time": end,
                "duration": end - start,
            }
        )
