from typing import Sequence
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph_swarm import create_swarm

from src.agents.chat.chat import ChatAgent
from src.agents.manage.manage import ManageAgent
from src.config.setup import GOOGLE_API_KEY


class Workflow:
    def __init__(self) -> None:
        self._checkpointer = MemorySaver()

        self._router_model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GOOGLE_API_KEY,
            disable_streaming=False,
        )

        self._agents: Sequence[CompiledStateGraph] = self._load_agents()

        self._app = self._build_app()

    def _load_agents(self) -> Sequence[CompiledStateGraph]:
        return [
            ChatAgent().get_agent(),
            ManageAgent().get_agent()
        ]

    def _build_app(self) -> CompiledStateGraph:
        return create_swarm(
            self._agents,
            default_active_agent="chat"
        ).compile(checkpointer=self._checkpointer)

    def get_agents(self) -> Sequence[CompiledStateGraph]:
        return self._agents

    def get_app(self) -> CompiledStateGraph:
        return self._app


app = Workflow()
graph = app.get_app()