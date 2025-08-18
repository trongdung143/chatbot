from typing import Sequence
from langchain_core.tools.base import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.agents.state import State
from src.config.setup import GOOGLE_API_KEY

# import tools
from src.tools.tranfers import transfer_to_chat
from src.tools.life import get_time, get_weather, get_relative_date
from src.tools.file import (
    save_upload_file,
    show_saved_file_folder,
    remove_file,
    rename_file,
    download_file,
    write_note,
    read_note,
)
from src.tools.system import (
    get_system_info,
    restart_server,
    open_application,
    close_application,
    shutdown_system,
    restart_system,
)
from src.tools.rag import rag_web, rag_file


class ManageAgent:
    def __init__(self):
        self._tools: Sequence[BaseTool] = [
            transfer_to_chat,
            get_time,
            get_weather,
            rag_web,
            get_relative_date,
            save_upload_file,
            show_saved_file_folder,
            remove_file,
            write_note,
            read_note,
            get_system_info,
            rename_file,
            restart_server,
            open_application,
            close_application,
            shutdown_system,
            restart_system,
            download_file,
            rag_file,
        ]

        self._model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GOOGLE_API_KEY,
            disable_streaming=False,
        ).bind_tools(self._tools)

        self._graph = self._build_graph()

    async def _manage(self, state: State) -> State:
        return {"messages": [await self._model.ainvoke(state["messages"])]}

    def _build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(State)
        graph.add_node("manage", self._manage)
        graph.add_node("tools", ToolNode(self._tools))
        graph.set_entry_point("manage")
        graph.add_conditional_edges("manage", tools_condition)
        graph.add_edge("tools", "manage")
        return graph.compile(name="manage")

    def get_agent(self) -> CompiledStateGraph:
        return self._graph

    def get_tools(self) -> Sequence[BaseTool]:
        return self._tools

    def get_builder(self) -> StateGraph:
        return self._graph.builder
