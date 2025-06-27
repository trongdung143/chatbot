from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Literal
from src.agents.state import State

from langgraph.types import interrupt, Command

# import tools
from src.tools.tranfers import transfer_to_manage
from src.prompts.prompts_read import read_prompt
from src.config.setup import GOOGLE_API_KEY

tools = [
    # transfer_to_manage,
]

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    disable_streaming=False,
).bind_tools(tools)


async def chat(state: State) -> State:
    return {"messages": [await model.ainvoke(state["messages"])]}


graph = StateGraph(State)

graph.add_node("chat", chat)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("chat")
graph.add_conditional_edges("chat", tools_condition)
graph.add_edge("tools", "chat")

agent = graph.compile(name="chat")
