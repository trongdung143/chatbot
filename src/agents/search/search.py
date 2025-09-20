from typing import Sequence
from langchain_core.tools.base import BaseTool
from time import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.search.prompt import prompt
from src.tools.life import get_relative_date, get_time


class SearchAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="search",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        task = state.get("results").get(state.get("prev_agent"))[-1]
        result = None
        response = await self._chain.ainvoke({"task": [HumanMessage(content=task)]})
        result = f"[Kết quả tìm kiếm] {response.content}"
        current_tasks = state.get("tasks", {})
        current_results = state.get("results", {})

        current_tasks.setdefault(self._agent_name, []).append(task)

        current_results.setdefault(self._agent_name, []).append(result)
        print("search")
        state.update(
            human=False,
            next_agent="writer",
            prev_agent=self._agent_name,
            tasks=current_tasks,
            results=current_results,
        )
        return state
