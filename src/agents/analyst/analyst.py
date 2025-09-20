from typing import Sequence
from time import time
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.analyst.prompt import prompt
from src.agents.human import human_node


class AnalystResponseFormat(BaseModel):
    content: str = Field(
        description="Phân tích lại yêu cầu một cách rõ ràng, có cấu trúc."
    )
    human: bool = Field(description="True nếu cần con người tham gia, False nếu không")


class AnalystAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="analyst",
            tools=tools,
            model=None,
        )

        self._prompt = prompt
        self._chain = self._prompt | self._model.with_structured_output(
            AnalystResponseFormat
        )
        self._set_subgraph()

    def _set_subgraph(self):
        self._sub_graph.add_node(self._agent_name, self.process)
        self._sub_graph.add_node("human_node", human_node)
        self._sub_graph.add_edge(self._agent_name, "human_node")
        self._sub_graph.set_entry_point(self._agent_name)

    async def process(self, state: State) -> State:
        response = await self._chain.ainvoke(
            {"task": [HumanMessage(content=state.get("task"))]}
        )
        print("analyst")
        state.update(
            messages=[response],
            agent_logs=state.get("agent_logs")
            + [
                {
                    "agent_name": "analyst",
                    "task": state.get("task"),
                    "result": response,
                }
            ],
            next_agent="supervisor",
            prev_agent="analyst",
            task=state.get("task"),
            result=response,
            human=response.human,
        )
        return state
