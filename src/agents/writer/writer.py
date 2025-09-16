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
        print("writer")
        start_time = time()

        if state["prev_agent"] == "assigner":
            response = await self._chain.ainvoke({"task": state["messages"]})
        else:
            annotated_msg = SystemMessage(
                content=f"NOTE: The following is the result from the {state["prev_agent"]} agent, not the user.\n"
            )
            response = await self._chain.ainvoke(
                {
                    "task": state["messages"]
                    + [annotated_msg, HumanMessage(content=state["task"])]
                }
            )
        print(response.content)
        end_time = time()

        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "writer",
                    "task": state["task"],
                    "result": response.content,
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": end_time - start_time,
                }
            ],
            prev_agent="writer",
            next_agent=None,
            human=False,
        )

        return {"messages": [response]}
