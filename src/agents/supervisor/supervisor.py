from typing import Sequence
from time import time
import json
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
            tools=tools or [],
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        start_time = time()
        response = await self._chain.ainvoke(
            {"supervision": [HumanMessage(content=state["task"])]}
        )
        direction = json.loads(response.content)
        end_time = time()
        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "supervisor",
                    "task": "direction",
                    "result": str(direction),
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": end_time - start_time,
                }
            ],
            next_agent=direction.get("next_agent"),
            prev_agent=state.get("prev_agent"),
            task=state.get("messages")[-1].content,
            human=direction.get("human"),
        )

        return state
