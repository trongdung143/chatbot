from typing import Sequence
from langchain_core.tools.base import BaseTool
from time import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    RemoveMessage,
)
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.memory.prompt import prompt


class MemoryAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="memory",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        print("memory")
        print(len(state.get("messages")))
        start_time = time()
        task = None
        if len(state.get("messages")) > 10:
            task = "summarize"
            response = await self._chain.ainvoke({"task": state.get("messages")[:-1]})
            return {
                "messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)],
                "summary": response.content,
                "task": task,
            }
        else:
            task = "skiped"
            response = SystemMessage(content="No summary needed (messages <= 10)")

        end_time = time()
        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "memory",
                    "task": task,
                    "result": response.content,
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": end_time - start_time,
                }
            ],
            next_agent="assigner",
            prev_agent="memory",
            task=task,
            human=False,
        )
        return state
