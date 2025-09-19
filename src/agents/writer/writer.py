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
        if state["prev_agent"] == "assigner":
            response = await self._chain.ainvoke({"task": state.get("messages")})
        else:
            annotated_msg = SystemMessage(
                content=f"NOTE: The following is the result from the {state.get("prev_agent")} agent, not the user.\n"
            )
            response = await self._chain.ainvoke(
                {
                    "task": state.get("messages")
                    + [annotated_msg, HumanMessage(content=state.get("result").content)]
                }
            )
        print("writer", response)
        print("length of messages: ", len(state.get("messages")))
        state.update(
            messages=[response],
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "writer",
                    "task": state.get("result"),
                    "result": response,
                }
            ],
            prev_agent="writer",
            next_agent=None,
            task=state.get("result"),
            result=response,
            human=False,
        )

        return state
