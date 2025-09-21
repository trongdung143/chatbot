from typing import Sequence
from time import time
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.emotive.prompt import prompt
from src.agents.utils import extract_text_from_pdf


class emotiveAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="emotive",
            tools=tools,
            model=None,
        )

        self._prompt = prompt
        self._chain = self._prompt | self._model
        self._set_subgraph()

    async def process(self, state: State) -> State:

        task = state.get("results").get(state.get("prev_agent"))[-1]
        result = None
        try:
            content = extract_text_from_pdf(state)
            response = await self._chain.ainvoke(
                {"task": [HumanMessage(content=f"[Nội Dung] {content}\n[Yêu Cầu] {task}")]}
            )
            result = response.content
            current_tasks, current_results = self.update_work(state, task, result)
            state.update(
                human=False,
                next_agent=None,
                prev_agent=self._agent_name,
                tasks=current_tasks,
                results=current_results,
            )
            print("emotive")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state
