from typing import Sequence
from langchain_core.tools.base import BaseTool
from time import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.planner.prompt import prompt
from src.tools.life import get_relative_date, get_time


class PlannerAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="planner",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        print("planner")
        start_time = time()
        response = await self._chain.ainvoke(
            {"task": [HumanMessage(content=state["task"])]}
        )
        print(response.content)
        end_time = time()
        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "planner",
                    "task": response.content,
                    "result": response.content,
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": end_time - start_time,
                }
            ],
            next_agent="writer",
            prev_agent="planner",
            task=response.content,
            human=None,
        )
        return state
