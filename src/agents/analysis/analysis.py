from typing import Sequence
from langchain_core.tools.base import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.agents.state import State
from src.config.setup import GOOGLE_API_KEY
from src.tools.tranfers import transfer_to_manage


class AnalysisAgent:
    def __init__(self) -> None:
        self._tools: Sequence[BaseTool] = []

        self._model = (ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GOOGLE_API_KEY,
            disable_streaming=False,

        ).bind_tools(self._tools))

        self._compiled_graph: CompiledStateGraph = self._build_graph()

    async def _analysis(self, state: State) -> State:
        return {"messages": [await self._model.ainvoke(state["messages"])]}

    def _build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(State)

        graph.add_node("analysis", self._analysis)
        graph.add_node("tools", ToolNode(self._tools))
        graph.set_entry_point("analysis")
        graph.add_conditional_edges("analysis", tools_condition)
        graph.add_edge("tools", "analysis")

        return graph.compile(name="analysis")

    def get_agent(self) -> CompiledStateGraph:
        return self._compiled_graph

    def get_tools(self) -> Sequence[BaseTool]:
        return self._tools

    def get_builder(self) -> StateGraph:
        return self._compiled_graph.builder
