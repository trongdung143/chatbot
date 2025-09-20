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
        response = await self._chain.ainvoke(
            {"supervision": [HumanMessage(content=task)]}
        )
        print("supervisor", response)
        result = f"[Từ kết quả phân tích của agent] {task} bạn hãy xử lý tiếp"
        current_tasks = state.get("tasks", {})
        current_results = state.get("results", {})

        current_tasks.setdefault(self._agent_name, []).append(task)

        current_results.setdefault(self._agent_name, []).append(result)
        state.update(
            human=False,
            next_agent=response.next_agent,
            prev_agent=self._agent_name,
            tasks=current_tasks,
            results=current_results,
        )

        return state
