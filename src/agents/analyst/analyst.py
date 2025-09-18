from typing import Sequence
from time import time

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.analyst.prompt import prompt


class AnalystResponse:
    pass


class AnalystAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="analyst",
            tools=tools,
            model=None,
        )

        self._prompt = prompt
        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        print("analyst")
        response = await self._chain.ainvoke(
            {"task": [HumanMessage(content=state.get("task"))]}
        )
        print("analyst", response.content)
        state.update(
            agent_logs=state.get("agent_logs")
            + [
                {
                    "agent_name": "analyst",
                    "task": state.get("task"),
                    "result": response.content,
                }
            ],
            next_agent=None,
            prev_agent="analyst",
            task=state.get("task"),
            result=response.content,
            human=None,
        )
        return state
