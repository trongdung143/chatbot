from typing import Sequence
from langchain_core.tools.base import BaseTool
from time import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.tool.prompt import prompt
from src.tools.life import get_relative_date, get_time


class ToolAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="tool",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:

        response = await self._chain.ainvoke(
            {"task": [HumanMessage(content=state.get("task"))]}
        )
        print("tool")
        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "tool",
                    "task": state.get("task"),
                    "result": response,
                }
            ],
            next_agent="writer",
            prev_agent="tool",
            task=state.get("task"),
            result=response,
            human=None,
        )
        return state
