from langgraph.graph import MessagesState
from typing import TypedDict
from pydantic import Field, BaseModel


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
    result: BaseModel
    human: bool
