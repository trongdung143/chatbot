from typing import Sequence
from time import time

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.state import State


class WriterAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="writer",
            tools=tools or [],
            model=None,
        )

        self._prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""  
                    You are the WRITER agent.
                    You should use the results from the previous agent's step and continue processing.
                    Your job: respond naturally and helpfully, based on the prior analysis or direct user message.
                """
                ),
                MessagesPlaceholder("task"),
            ]
        )

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        start_time = time()

        task_msg = HumanMessage(content=state["task"])

        response = await self._chain.ainvoke({"task": state["messages"] + [task_msg]})
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

        return {"messages": [response]}
