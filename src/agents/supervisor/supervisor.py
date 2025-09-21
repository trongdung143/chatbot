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
        task = state.get("results").get(state.get("prev_agent"))[-1]
        result = None
        try:
            response = await self._chain.ainvoke(
                {"supervision": [HumanMessage(content=task)]}
            )

            result = f"[Từ kết quả] {task}"
            current_tasks, current_results = self.update_work(state, task, result)
            state.update(
                human=False,
                next_agent=response.next_agent,
                prev_agent=self._agent_name,
                tasks=current_tasks,
                results=current_results,
            )
            print("supervisor")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state
