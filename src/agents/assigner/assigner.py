from typing import Sequence
from time import time
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import SystemMessage, HumanMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.assigner.prompt import prompt


class AssignerResponseFormat(BaseModel):
    next_agent: str = Field(
        description="Tên agent tiếp theo, 'analyst', 'coder', 'planner', 'search', 'tool', 'vision', 'writer', 'emotive'"
    )
    content: str = Field(description="Chuyển yêu cầu cho agent khác xử lý.")


class AssignerAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="assigner",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model.with_structured_output(
            AssignerResponseFormat
        )

    async def process(self, state: State) -> State:
        task = state.get("results").get(state.get("prev_agent"))[-1]
        result = None
        try:
            response = await self._chain.ainvoke({"assignment": [HumanMessage(content=task)]})
            result = f"### Phân công (assigner)\n{response.next_agent}"

            current_tasks, current_results = self.update_work(state, task, result)
            state.update(
                human=False,
                next_agent=response.next_agent.strip(),
                prev_agent=state.get("prev_agent"),
                tasks=current_tasks,
                results=current_results,
            )
            print("assigner")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state
