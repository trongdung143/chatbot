from typing import Sequence
from time import time

from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.writer.prompt import prompt
from src.agents.state import State


class WriterAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="writer",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        task = state.get("results").get(state.get("prev_agent"))[-1]
        result = None
        if state["prev_agent"] == "assigner":
            response = await self._chain.ainvoke({"task": state.get("messages")})
        else:
            response = await self._chain.ainvoke(
                {
                    "task": [
                        HumanMessage(
                            content=f"Từ kết quả của agent trước hãy xử lý tiếp {task}"
                        )
                    ]
                }
            )
        result = response.content
        print("writer")
        print("length of messages: ", len(state.get("messages")))
        current_tasks = state.get("tasks", {})
        current_results = state.get("results", {})

        current_tasks.setdefault(self._agent_name, []).append(task)

        current_results.setdefault(self._agent_name, []).append(result)
        state.update(
            messages=[response],
            human=False,
            prev_agent=self._agent_name,
            next_agent=None,
            tasks=current_tasks,
            results=current_results,
        )

        return state
