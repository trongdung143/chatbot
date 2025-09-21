from langgraph.graph import MessagesState
from typing import TypedDict
from pydantic import Field, BaseModel
from langchain_core.messages import BaseMessage
import os


class State(MessagesState):
    thread_id: str
    human: bool
    next_agent: str | None
    prev_agent: str | None
    tasks: dict[str, list[str]] = Field(default_factory=dict)
    results: dict[str, list[str]] = Field(default_factory=dict)
    file_path: str | None = None
