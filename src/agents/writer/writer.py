from typing import Sequence
from time import time

from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.writer.prompt import prompt
from src.agents.state import State
from langsmith import traceable


class WriterAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="writer",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    @traceable
    async def process(self, state: State) -> State:
        task = state.get("results").get(state.get("prev_agent"))[-1]
        result = None
        try:
            if state["prev_agent"] == "assigner":
                response = await self._chain.ainvoke({"task": state.get("messages")})
            else:
                response = await self._chain.ainvoke(
                    {
                        "task": [
                            HumanMessage(
                                content=f"Từ kết quả của agent trước hãy trả lời {task}"
                            )
                        ]
                    }
                )
            result = response.content
            current_tasks, current_results = self.update_work(state, task, result)
            state.update(
                messages=[response],
                human=False,
                prev_agent=self._agent_name,
                next_agent=None,
                tasks=current_tasks,
                results=current_results,
            )
            print("writer")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state
