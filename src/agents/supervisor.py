from typing import Sequence
from time import time

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool

from src.agents.base import BaseAgent
from src.agents.state import State


class SupervisorAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="supervisor",
            tools=tools or [],
            model=None,
        )

        self._prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are the SUPERVISOR agent.\n"
                    "Your job: decide which specialized agent should handle the user's last message.\n\n"
                    "Rules:\n"
                    "- If the request is casual conversation, chit-chat, or simple → respond ONLY with: writer\n"
                    "- If the request is complex, requires reasoning, problem-solving, or analysis → respond ONLY with: analysis\n\n"
                    "IMPORTANT: Output exactly one word: 'writer' or 'analysis'.",
                ),
                MessagesPlaceholder("assignment"),
            ]
        )

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        start_time = time()

        latest_user_msg = state["messages"][-1]

        response = await self._chain.ainvoke({"assignment": [latest_user_msg]})
        predicted_agent = response.content.strip().lower()

        end_time = time()
        duration = end_time - start_time

        state["next_agent"] = predicted_agent
        state["task"] = latest_user_msg.content
        state["prev_agent"] = "supervisor"

        state["agent_logs"].append(
            {
                "agent_name": "supervisor",
                "task": latest_user_msg.content,
                "result": predicted_agent,
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
            }
        )
        return state
