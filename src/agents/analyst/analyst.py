from typing import Sequence
from time import time

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.analyst.prompt import prompt


class AnalystResponse:
    pass


class AnalystAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="analyst",
            tools=tools or [],
            model=None,
        )

        self._prompt = prompt
        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        start_time = time()

        task_msg = HumanMessage(content=state["task"])

        response = await self._chain.ainvoke({"task": [task_msg]})
        analysis_result = response.content

        end_time = time()
        duration = end_time - start_time

        state["agent_logs"].append(
            {
                "agent_name": "analyst",
                "task": state["task"],
                "result": analysis_result,
                "step": len(state["agent_logs"]),
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
            }
        )

        state["task"] = analysis_result
        state["prev_agent"] = "analyst"
        state["next_agent"] = "calculator"

        return state
