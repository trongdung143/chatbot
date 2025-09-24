from typing import Sequence
from langchain_core.tools.base import BaseTool
from time import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.coder.prompt import prompt


class CoderAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="coder",
            tools=tools,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        tasks = state.get("assigned_agents").get(self._agent_name)
        task = ""
        for t in tasks:
            task = task + f"{t}\n"
        result = None
        try:
            response = await self._chain.ainvoke({"task": [HumanMessage(content=task)]})
            result = f"### Kết quả code (coder)\n{response.content}"
            current_tasks, current_results, assigned_agents = self.update_work(state, task, result)
            state.update(
                human=False,
                prev_agent=self._agent_name,
                tasks=current_tasks,
                results=current_results,
                assigned_agents=assigned_agents,
            )
            print("coder")
        except Exception as e:
            print("ERROR ", self._agent_name)
        return state
