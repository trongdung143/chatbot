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
        task = state.get("results").get(state.get("prev_agent"))[-1]
        result = None
        try:
            response = await self._chain.ainvoke({"task": state.get("messages")})
            result = f"[Phân tích yêu cầu cầu người dùng] {response.content}"
            current_tasks, current_results = self.update_work(state, task, result)
            state.update(
                messages=[AIMessage(content=response.content)],
                human=response.human,
                next_agent="supervisor",
                prev_agent=self._agent_name,
                tasks=current_tasks,
                results=current_results,
            )
            print("analyst")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state
