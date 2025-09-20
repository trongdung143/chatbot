from typing import Sequence
from time import time
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import SystemMessage, HumanMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.assigner.prompt import prompt


class AssignerResponseFormat(BaseModel):
    next_agent: str = Field(
        description="Tên agent tiếp theo, 'analyst', 'coder', 'planner', 'search', 'tool', 'vision', 'writer', 'emotive'"
    )
    content: str = Field(description="không trả lời, không giải thích gì cả")


class AssignerAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="assigner",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model.with_structured_output(
            AssignerResponseFormat
        )

    async def process(self, state: State) -> State:

        response = await self._chain.ainvoke({"assignment": state.get("messages")})
        print("assigner", response.next_agent)
        state.update(
            agent_logs=state.get("agent_logs", [])
            + [
                {
                    "agent_name": "assigner",
                    "task": state.get("messages")[-1].content,
                    "result": response,
                }
            ],
            next_agent=response.next_agent,
            prev_agent="assigner",
            task=state.get("messages")[-1].content,
            result=response,
            human=False,
        )

        return state
