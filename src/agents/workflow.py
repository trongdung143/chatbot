from langgraph.checkpoint.memory import MemorySaver
from langgraph_swarm import create_swarm
from src.agents.chat.chat import agent as agent2
from src.agents.manage.manage import agent as agent1

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


workflow = create_swarm([agent1, agent2], default_active_agent="chat")

swarm = workflow.compile(checkpointer=checkpointer)
