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

        response = await self._chain.ainvoke(
            {"task": [HumanMessage(content=state.get("task"))]}
        )
        print("search", response.content)
        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "search",
                    "task": response.content,
                    "result": response.content,
                }
            ],
            next_agent="writer",
            prev_agent="search",
            task=state.get("task"),
            result=response.content,
            human=None,
        )
        return state
