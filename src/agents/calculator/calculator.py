from typing import Sequence
from langchain_core.tools.base import BaseTool
from time import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.calculator.prompt import prompt


class CalculatorAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="calculator",
            tools=tools or [],
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        start_time = time()

        task_msg = HumanMessage(content=state["task"])
        response = await self._chain.ainvoke({"task": [task_msg]})
        logic_result = response.content.strip() if response.content else ""

        end_time = time()
        duration = end_time - start_time

        final_task = state["task"] if logic_result == "" else logic_result

        state["agent_logs"].append(
            {
                "agent_name": "calculator",
                "task": state["task"],
                "result": logic_result,
                "step": len(state["agent_logs"]),
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
            }
        )

        state["task"] = final_task
        state["prev_agent"] = "calculator"
        state["next_agent"] = "writer"

        return state
