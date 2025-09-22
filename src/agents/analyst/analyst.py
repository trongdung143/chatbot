from typing import Sequence
from time import time
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.types import interrupt, Command
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.analyst.prompt import prompt
from src.agents.supervisor.supervisor import SupervisorAgent

# class AnalystResponseFormat(BaseModel):
#     content: str = Field(
#         description="Phân tích lại yêu cầu một cách rõ ràng, có cấu trúc."
#     )
#     human: bool = Field(description="True nếu cần con người tham gia, False nếu không")
#     next_agent: str = Field(description="Nếu sau khi phân tích cần tính toán thì chọn 'calculator', ngược lại 'writer'")

class AnalystAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="analyst",
            tools=tools,
            model=None,
        )

        self._prompt = prompt
        self._chain = self._prompt | self._model
        self._supervisor = SupervisorAgent()
        self._set_subgraph()

    def _set_subgraph(self):
        self._sub_graph.add_node("llm_node", self._llm_node)
        self._sub_graph.add_node("human_node", self._human_node)
        self._sub_graph.add_node("supervisor_node", self._supervisor.process)
        self._sub_graph.set_entry_point("llm_node")
        self._sub_graph.add_edge("llm_node", "supervisor_node")
        self._sub_graph.add_conditional_edges(
            "supervisor_node",
            self._route,
            {"human_node": "human_node", "llm_node": "llm_node", "__end__": "__end__"}
        )
        self._sub_graph.add_edge("human_node", "__end__")

    def _route(self, state: State) -> str:
        if state.get("human") is True:
            return "human_node"
        else:
            if state.get("next_agent") in ["calculator", "writer"]:
                return "__end__"
            elif state.get("next_agent") == "analyst":
                return "llm_node"
            elif state.get("next_agent") == "supervisor":
                return "supervisor_node"

    def _human_node(self, state: State) -> State:
        if state.get("human") is True:
            print("human")
            task = state.get("results").get(state.get("prev_agent"))[-1]
            marker = "### Phân tích yêu cầu cầu (analyst)"
            analyst_part = None
            if marker in task:
                analyst_part = task.split(marker, 1)[-1].strip()
            edit = interrupt({"AIMessage": analyst_part})
            task = f"{task}\n\n### Yêu cầu bổ sung (user)\n{edit}"
            result = state.get("results").get(state.get("prev_agent"))
            result[-1] = task
            current_results = state.get("results")
            current_results[state.get("prev_agent")] = result
            state.update(results=current_results, human=False)
        return state

    async def _llm_node(self, state: State) -> State:
        task = state.get("results").get(state.get("prev_agent"))[-1]
        result = None
        try:
            if state.get("prev_agent") != "supervisor":
                response = await self._chain.ainvoke({"task": [HumanMessage(content=f"{task}")]})
                result = f"### Phân tích yêu cầu cầu (analyst)\n{response.content}"
                current_tasks, current_results = self.update_work(state, task, result)
                state.update(
                    messages=[AIMessage(content=response.content)],
                    next_agent="supervisor",
                    prev_agent=self._agent_name,
                    tasks=current_tasks,
                    results=current_results,
                )
            else:
                message = HumanMessage(content=f"{task}")
                response = await self._chain.ainvoke({"task": [HumanMessage(content=f"{state.get("results").get(state.get(self._agent_name))[-1]}\n\n{task}\n\n### Từ feedback hãy sửa lại phân tích.")]})
                result = f"### Phân tích lại yêu cầu (analyst)\n{response.content}"
                current_tasks, current_results = self.update_work(state, task, result)
                state.update(
                    messages=[message,
                              AIMessage(content=response.content)],
                    next_agent="supervisor",
                    prev_agent=self._agent_name,
                    tasks=current_tasks,
                    results=current_results,
                )
            print("analyst")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state

    async def process(self, state: State) -> State:
        sub_graph = self.get_subgraph()
        response = await sub_graph.ainvoke(state)
        state = response
        return state

