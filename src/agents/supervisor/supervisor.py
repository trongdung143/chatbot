from typing import Sequence
from time import time
import re, json


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool

from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.supervisor.prompt import prompt
from langchain_core.messages import HumanMessage


class SupervisorAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="supervisor",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:

        response = await self._chain.ainvoke(
            {"supervision": [HumanMessage(content=state.get("result"))]}
        )
        print("supervisor", response.content)

        direction = json.loads(response.content.strip())
        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "supervisor",
                    "task": "direction",
                    "result": str(direction),
                }
            ],
            next_agent=direction.get("next_agent"),
            prev_agent=state.get("prev_agent"),
            task=state.get("result"),
            result=response.content,
            human=direction.get("human"),
        )

        return state
