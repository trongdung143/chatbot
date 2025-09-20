from typing import Sequence
from time import time
import re, json
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool


from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.supervisor.prompt import prompt
from langchain_core.messages import HumanMessage


class SupervisorResponseFormat(BaseModel):
    next_agent: str = Field(description="Tên agent tiếp theo 'calculator', 'writer'")
    content: str = Field(description="không trả lời, không giải thích gì cả")


class SupervisorAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="supervisor",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model.with_structured_output(
            SupervisorResponseFormat
        )

    async def process(self, state: State) -> State:

        response = await self._chain.ainvoke(
            {"supervision": [HumanMessage(content=state.get("result").content)]}
        )
        print("supervisor", response)

        state.update(
            messages=[state.get("result").content],
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "supervisor",
                    "task": "direction",
                    "result": response,
                }
            ],
            next_agent=response.next_agent,
            prev_agent=state.get("prev_agent"),
            task=state.get("result"),
            result=response,
            human=False,
        )

        return state
