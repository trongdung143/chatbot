from typing import Sequence
from langchain_core.tools.base import BaseTool
from time import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.calculator.prompt import prompt
from src.tools.life import get_relative_date, get_time


class CalculatorAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="calculator",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        task = state.get("results").get(state.get("prev_agent"))[-1]
        result = None
        try:
            response = await self._chain.ainvoke({"task": [HumanMessage(content=task)]})
            result = f"### Kết quả tính toán (calculator)\n{response.content}"

            current_tasks, current_results = self.update_work(state, task, result)
            state.update(
                human=False,
                next_agent="writer",
                prev_agent=self._agent_name,
                tasks=current_tasks,
                results=current_results,
            )
            print("calculator")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state
