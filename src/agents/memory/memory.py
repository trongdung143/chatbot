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

        task = None
        response = None
        messages = state.get("messages")
        if len(messages) >= 10:
            last_msg = messages[-1]
            task = "summary"
            response = await self._chain.ainvoke({"task": messages[:-1]})
            delete_msg = [RemoveMessage(id=REMOVE_ALL_MESSAGES)]
            messages = delete_msg + [SystemMessage(content=response.content), last_msg]
        else:
            task = "skiped"
            response = SystemMessage(content="messages < 10")
        print("memory", response.content)
        state.update(
            messages=messages,
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "memory",
                    "task": task,
                    "result": response,
                }
            ],
            next_agent="assigner",
            prev_agent="memory",
            task=task,
            result=response,
            human=False,
        )
        return state
