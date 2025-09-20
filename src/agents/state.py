from langgraph.graph import MessagesState
from typing import TypedDict
from pydantic import Field, BaseModel
from langchain_core.messages import BaseMessage
import os

agents_dir = "src/agents"

agents = [
    name
    for name in os.listdir(agents_dir)
    if os.path.isdir(os.path.join(agents_dir, name))
]


class AgentLog(TypedDict):
    agent_name: str
    task: str
    result: BaseModel


class State(MessagesState):
    thread_id: str
    agent_logs: list[AgentLog] = Field(default_factory=list)
    next_agent: str
    prev_agent: str
    task: str
    result: BaseModel | str | BaseMessage
    human: bool
    file_path: str | None = None


# class State1(MessagesState):
#     thread_id: str
#     agent_logs: list[dict] = Field(default_factory=list)
#     next_agent: str | None = None
#     prev_agent: str | None = None
#     tasks: dict[str, list[str]] = Field(default_factory=dict)
#     results: dict[str, list[str]] = Field(default_factory=dict)
