from typing import Sequence
from time import time

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.agents.base import BaseAgent
from src.agents.state import State


class AnalysisAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="analysis",
            tools=tools or [],
            model=None,
        )

        self._prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""
                You are the ANALYSIS agent.
                Your task: analyze the user's request only.
                Be concise, structured, and focus on reasoning or problem-solving steps.
                Do not generate the final answer or solution — only break down the request into what needs to be done.
                """
                ),
                MessagesPlaceholder("task"),
            ]
        )

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
                "agent_name": "analysis",
                "task": state["task"],
                "result": analysis_result,
                "step": len(state["agent_logs"]),
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
            }
        )

        state["task"] = analysis_result
        state["prev_agent"] = "analysis"
        state["next_agent"] = "logic"

        return state
