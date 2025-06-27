from typing import Any, Coroutine

from langchain_core.messages import BaseMessage
from langgraph_swarm import create_swarm
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from src.agents.manage.manage import agent as agent1
from src.agents.chat.chat import agent as agent2
from src.agents.state import State
from src.config.setup import GOOGLE_API_KEY
from langchain_core.messages import SystemMessage
from langgraph.types import interrupt, Command
#
# model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=GOOGLE_API_KEY,
#     disable_streaming=False,
# )
#
#
# async def supervisor(state: State):
#     resp = await model.ainvoke(state["messages"] + [SystemMessage(
#         content="""You are a routing expert, read the user's content and return a word: "chat" if it is a normal chat request or "manage" if it is a task management request, handle the request from the system.""")])
#     print(resp)
#     resp = resp.content.strip()
#
#     if "chat" == resp:
#         return Command(goto="chat",
#                        update={"active_agent": "chat", "messages": [resp] + state["messages"]}, )
#     elif "manage" == resp:
#         return Command(goto="manage",
#                        update={"active_agent": "manage", "messages": [resp] + state["messages"]}, )
#
#     return Command(goto="chat", update={"active_agent": "chat", "messages": [resp] + state["messages"]})
#
#
checkpointer = MemorySaver()
#
# workflow = StateGraph(State)
# workflow.add_node("manage", agent1)
# workflow.add_node("chat", agent2)
#
# workflow.add_node("supervisor", supervisor)
# workflow.set_entry_point("supervisor")
#
# swarm = workflow.compile(checkpointer=checkpointer)


workflow = create_swarm([agent1, agent2],default_active_agent="chat")

swarm = workflow.compile(checkpointer=checkpointer)