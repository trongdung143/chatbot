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
        print("emotive")
        content = extract_text_from_pdf(state)
        print(content)
        response = await self._chain.ainvoke(
            {
                "task": [
                    HumanMessage(
                        content=f"[Nội Dung]\n{content}\n[Yêu Cầu]\n{state.get('task')}"
                    )
                ]
            }
        )
        state.update(
            agent_logs=state.get("agent_logs")
            + [
                {
                    "agent_name": "emotive",
                    "task": state.get("task"),
                    "result": response,
                }
            ],
            next_agent=None,
            prev_agent="emotive",
            task=state.get("task"),
            result=response,
            human=False,
        )
        return state
