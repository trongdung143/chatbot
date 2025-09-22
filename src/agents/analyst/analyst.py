from typing import Sequence
from time import time
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.types import interrupt, Command
from streamlit import feedback

from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.analyst.prompt import prompt, prompt_supervisor
from src.agents.supervisor.supervisor import SupervisorAgent

class AnalystState(dict):
    task: str
    result: str
    feedback: str
    analysis: str
    human: bool
    next_agent: str
    prev_agent: str

class SupervisorResponseFormatForAnalyst(BaseModel):
    next_agent: str = Field(description="Tên agent tiếp theo 'calculator', 'writer', 'analyst'")
    content: str = Field(description="Feedback cho agent biết điểm chưa hoàn thành tốt.")
    human: bool = Field(description="Nếu cần sự can thiệp của con người 'human' là True, ngược lại là False")


class SupervisorForAnalyst(SupervisorAgent):
    def __init__(self):
        super().__init__(state=AnalystState, prompt=prompt_supervisor, response_format=SupervisorResponseFormatForAnalyst)

    async def process(self, state: AnalystState) -> AnalystState:
        task = None
        result = None
        try:
            task = state.get("analysis")
            response = await self._chain.ainvoke(
                {"supervision": [HumanMessage(content=f"{task}")]}
            )

            result = f"### Feedback (supervisor)\n{response.content}"
            if response.next_agent == state.get("prev_agent"):
                state.update(feedback=result)
            elif response.next_agent in ["writer", "calculator"]:
                state.update(
                    human=response.human,
                    next_agent=response.next_agent,
                    result=state.get("result"),
                )

            print("supervisor")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state


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
            state=AnalystState,
            model=None,
        )

        self._prompt = prompt
        self._chain = self._prompt | self._model
        self._supervisor = SupervisorForAnalyst()
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

    def _route(self, state: AnalystState) -> str:
        if state.get("human") is True:
            return "human_node"
        else:
            if state.get("next_agent") in ["calculator", "writer"]:
                return "__end__"
            elif state.get("next_agent") == "analyst":
                return "llm_node"
            elif state.get("next_agent") == "supervisor":
                return "supervisor_node"

    def _human_node(self, state: AnalystState) -> AnalystState:
        if state.get("human") is True:
            print("human")
            task = state.get("analysis")
            marker = "### Phân tích yêu cầu cầu (analyst)"
            analyst_part = None
            if marker in task:
                analyst_part = task.split(marker, 1)[-1].strip()
            edit = interrupt({"AIMessage": analyst_part})
            result = f"{task}\n\n### Yêu cầu bổ sung\n{edit}"
            state.update(
                result=result,
            )
        return state

    async def _llm_node(self, state: AnalystState) -> AnalystState:
        result = None
        try:
            if state.get("prev_agent") != "supervisor":
                task = state.get("task")
                response = await self._chain.ainvoke({"task": [HumanMessage(content=f"{task}")]})
                result = f"### Phân tích yêu cầu cầu (analyst)\n{response.content}"
                state.update(
                    analysis=result,
                    next_agent="supervisor",
                    prev_agent=self._agent_name,
                    result=response.content,
                )
            else:
                feedback = state.get("feedback")
                analysis = state.get("analysis")
                response = await self._chain.ainvoke({"task": [HumanMessage(content=f"{analysis}\n\n{feedback}\n\n### Từ feedback hãy sửa lại phân tích.")]})
                result = f"### Phân tích lại yêu cầu {response.content}"
                state.update(
                    analysis=result,
                    next_agent="supervisor",
                    prev_agent=self._agent_name,
                    result=response.content,
                )
            print("analyst")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state

    async def process(self, state: State) -> State:
        task = state.get("results").get(state.get("prev_agent"))[-1]
        input_state = {
            "task": task,
            "result": None,
            "feedback": None,
            "analysis": None,
            "human": False,
            "next_agent": None,
            "prev_agent": state.get("prev_agent"),
        }
        sub_graph = self.get_subgraph()
        response = await sub_graph.ainvoke(input=input_state)
        current_tasks, current_results = self.update_work(state, task, response.get("result"))
        state.update(
            human=False,
            next_agent=response.get("next_agent"),
            prev_agent=self._agent_name,
            tasks=current_tasks,
            results=current_results,
        )
        return state

