from typing import Sequence
from time import time

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool

from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.assigner.prompt import prompt


class AssignerAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="assigner",
            tools=tools or [],
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        message = state.get("messages")[-1]
        start_time = time()
        response = await self._chain.ainvoke({"assignment": state["messages"]})
        end_time = time()
        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "assigner",
                    "task": state["messages"][-1].content,
                    "result": response.content,
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": end_time - start_time,
                }
            ],
            next_agent=response.content.strip(),
            prev_agent="assigner",
            task=message.content,
            human=False,
        )

        return state
