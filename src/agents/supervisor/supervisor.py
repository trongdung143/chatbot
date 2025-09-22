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
    next_agent: str = Field(description="Tên agent tiếp theo 'calculator', 'writer', 'analyst'")
    content: str = Field(description="Feedback cho agent biết điểm chưa hoàn thành tốt.")
    human: bool = Field(description="Nếu cần sự can thiệp của con người 'human' là True, ngược lại là False")


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
            if state.get("prev_agent") == "analyst":
                response = await self._chain.ainvoke(
                    {"supervision": [HumanMessage(content=f"### kết quả của agent analyst\n{task}")]}
                )

                result = f"### Feedback (supervisor)\n{response.content}"
                current_tasks, current_results = self.update_work(state, task, result)
                prev_agent = None
                if response.next_agent in ["writer", "calculator"]:
                    prev_agent = state.get("prev_agent")
                else:
                    prev_agent = self._agent_name
                state.update(
                    human=response.human,
                    next_agent=response.next_agent,
                    prev_agent=prev_agent,
                    tasks=current_tasks,
                    results=current_results,
                )
            else:
                pass

            print("supervisor")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state
