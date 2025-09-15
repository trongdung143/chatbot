from langgraph.graph import MessagesState
from typing import TypedDict
from pydantic import Field
import json


class AgentLog(TypedDict):
    agent_name: str
    task: str
    result: str
    start_time: float
    end_time: float
    duration: float


class State(MessagesState):
    thread_id: str
    agent_logs: list[AgentLog] = Field(default_factory=list)
    next_agent: str
    prev_agent: str
    task: str
    human: bool
