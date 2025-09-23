from typing import Sequence

from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.tools.base import BaseTool
from langgraph.types import interrupt
from pydantic import BaseModel, Field

from src.agents.analyst.prompt import prompt, prompt_supervisor
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.supervisor.supervisor import SupervisorAgent

ANALYSIS = "### Phân tích yêu cầu (analyst)"
TRY_ANALYSIS = "### Phân tích lại yêu cầu (analyst)"

class AnalystState(dict):
    messages: list[BaseMessage]
    task: str
    result: str
    feedback: str
    analysis: str
    next_agent: str
    prev_agent: str

class SupervisorResponseFormatForAnalyst(BaseModel):
    next_agent: str = Field(description="'next_agent' là 'human_node', 'llm_node', '__end__'")
    content: str = Field(description="Feedback cho agent biết điểm chưa hoàn thành tốt.")


class SupervisorForAnalyst(SupervisorAgent):
    def __init__(self):
        super().__init__(state=AnalystState, prompt=prompt_supervisor, response_format=SupervisorResponseFormatForAnalyst)

    async def process(self, state: AnalystState) -> AnalystState:
        try:
            task = state.get("task")
            analysis = state.get("analysis")
            response = await self._chain.ainvoke(
                {"supervision": [HumanMessage(content=f"### Yêu cầu (user)\n{task}\n\n{analysis}")]}
            )

            feedback = f"### Feedback (supervisor)\n{response.content}"

            if response.next_agent == "llm_node":
                state.update(
                    feedback=feedback,
                    prev_agent="supervisor_node",
                    next_agent="llm_node",
                )
            elif response.next_agent == "human_node":
                state.update(
                    result=analysis,
                    next_agent="human_node",
                )
            elif response.next_agent == "__end__":
                state.update(
                    result=analysis,
                    next_agent="__end__",
                )

            print("supervisor_node in analyst agent")
        except Exception as e:
            print("ERROR ", "supervisor_node in analyst agent\n", e)
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
        next_agent = state.get("next_agent").strip()
        VALID_AGENTS = [
            "llm_node",
            "human_node",
            "__end__"
        ]
        if next_agent in VALID_AGENTS:
            return next_agent
        return "__end__"

    def _human_node(self, state: AnalystState) -> AnalystState:

        analysis = state.get("analysis")
        marker = [ANALYSIS, TRY_ANALYSIS]
        analysis_part = None
        for mark in marker:
            if mark in analysis:
                analysis_part = analysis.split(mark, 1)[-1].strip()
                break
        edit = interrupt({"AIMessage": analysis_part})
        result = f"{ANALYSIS}\n{analysis_part}\n\n### Yêu cầu bổ sung (user)\n{edit}"
        state.update(
            result=result,
        )
        print("human_node in analyst agent")


        return state

    async def _llm_node(self, state: AnalystState) -> AnalystState:
        try:
            result = None
            if state.get("prev_agent") != "supervisor_node":
                response = await self._chain.ainvoke({"task": state.get("messages")})
                analysis = f"{ANALYSIS}\n{response.content}"
                state.update(
                    analysis=analysis,
                    next_agent="supervisor_node",
                    prev_agent="llm_node",
                )
            elif state.get("prev_agent") == "supervisor_node":
                feedback = state.get("feedback")
                analysis = state.get("analysis")
                response = await self._chain.ainvoke({"task": [HumanMessage(content=f"{analysis}\n\n{feedback}\n\n### Từ feedback hãy sửa lại phân tích.")]})
                analysis = f"{TRY_ANALYSIS}\n{response.content}"
                state.update(
                    analysis=analysis,
                    next_agent="supervisor_node",
                    prev_agent="llm_node",
                )
            print("llm_node in analyst agent")
        except Exception as e:
            print("ERROR ", "llm_node in analyst agent\n", e)
        return state

    async def process(self, state: State) -> State:
        messages = state.get("messages")
        task = messages[-1].content
        input_state = {
            "messages": messages,
            "task": task,
            "result": None,
            "feedback": None,
            "analysis": None,
            "next_agent": None,
            "prev_agent": state.get("prev_agent"),
        }
        sub_graph = self.get_subgraph()
        response = await sub_graph.ainvoke(input=input_state)
        current_tasks, current_results = self.update_work(state, task, response.get("result"))
        state.update(
            human=False,
            next_agent="assigner",
            prev_agent=self._agent_name,
            tasks=current_tasks,
            results=current_results,
        )
        return state

