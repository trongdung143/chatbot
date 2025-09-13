from typing import Sequence
from langchain_core.tools.base import BaseTool
from time import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.state import State


class LogicAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="logic",
            tools=tools or [],
            model=None,
        )

        self._prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""
                You are the LOGIC/MATH agent.
                You should use the results from the previous agent's step and continue processing.
                Goal:
                - If the user's request clearly involves mathematics (arithmetic, algebra, calculus, probability, statistics, unit conversion, dimensional analysis, etc.), then you must SOLVE it carefully following the rules below.
                - If the request DOES NOT contain any mathematical or logical problems, do not attempt to answer. Instead, return NO_MATH.
                This tag indicates the supervisor should route the request to another agent.

                Rules for solving math:
                1) Work carefully and compute digit-by-digit where needed; keep units and significant figures consistent.
                2) State minimal assumptions only when data is missing/ambiguous; never invent data.
                3) Prefer exact forms (fractions, radicals) unless a decimal is requested; if rounding, specify the rule.
                4) Provide a brief structured result:
                - Answer: <final value with units if any>
                - Justification: 2-4 concise steps (no long chain-of-thought)
                - Check: a quick verification (plug back / dimension / sanity)
                5) If multiple sub-parts, label (a), (b), (c) clearly.
                6) Mirror the user's language (Vietnamese or English).
                7) Do not use external tools or the web.
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
        logic_result = response.content

        end_time = time()
        duration = end_time - start_time

        if "NO_MATH" in logic_result:
            final_task = state["task"]
        else:
            final_task = logic_result

        state["agent_logs"].append(
            {
                "agent_name": "logic",
                "task": state["task"],
                "result": logic_result,
                "step": len(state["agent_logs"]),
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
            }
        )

        state["task"] = final_task
        state["prev_agent"] = "logic"
        state["next_agent"] = "writer"

        return state
