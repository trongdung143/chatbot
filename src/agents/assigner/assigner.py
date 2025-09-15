from typing import Sequence
from time import time

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool

from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.assigner.prompt import prompt


class AssignerAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="assigner",
            tools=tools or [],
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        start_time = time()

        latest_user_msg = state["messages"][-1]

        response = await self._chain.ainvoke({"assignment": state["messages"]})
        predicted_agent = response.content.strip().lower()

        end_time = time()
        duration = end_time - start_time

        state["next_agent"] = predicted_agent
        state["task"] = latest_user_msg.content
        state["prev_agent"] = "assigner"

        state["agent_logs"].append(
            {
                "agent_name": "assigner",
                "task": latest_user_msg.content,
                "result": predicted_agent,
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
            }
        )
        state["human"] = False

        return state
