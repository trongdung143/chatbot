from typing import Sequence
from time import time

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import SystemMessage, HumanMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.assigner.prompt import prompt


class AssignerAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="assigner",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:

        response = await self._chain.ainvoke({"assignment": state.get("messages")})
        print("assigner", response.content.strip())
        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "assigner",
                    "task": state.get("messages")[-1].content,
                    "result": response.content.strip(),
                }
            ],
            next_agent=response.content.strip(),
            prev_agent="assigner",
            task=state.get("messages")[-1].content,
            result=response.content.strip(),
            human=False,
        )

        return state
