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
            tools=tools or [],
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        start_time = time()

        task_msg = HumanMessage(content=state["task"])

        if state["prev_agent"] == "assigner":
            response = await self._chain.ainvoke(
                {"task": state["messages"] + [task_msg]}
            )
        else:
            annotated_msg = SystemMessage(
                content=f"NOTE: The following is the result from the {state["prev_agent"]} agent, not the user.\n"
            )
            response = await self._chain.ainvoke(
                {"task": state["messages"] + [annotated_msg, task_msg]}
            )

        writer_result = response.content

        end_time = time()
        duration = end_time - start_time

        state["agent_logs"].append(
            {
                "agent_name": "writer",
                "task": state["task"],
                "result": writer_result,
                "step": len(state["agent_logs"]),
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
            }
        )

        state["prev_agent"] = "writer"
        state["next_agent"] = None
        state["human"] = False

        return {"messages": [response]}
