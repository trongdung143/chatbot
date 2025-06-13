from langgraph_swarm import SwarmState, add_active_agent_router
from langgraph.checkpoint.memory import MemorySaver
from src.agents.manage import agent as agent1
from src.agents.chat import agent as agent2
from langgraph.graph import StateGraph

checkpointer = MemorySaver()


workflow = (
    StateGraph(SwarmState)
    .add_node(agent1, destinations=("chat",))
    .add_node(agent2, destinations=("manage",))
)

workflow = add_active_agent_router(
    builder=workflow,
    route_to=["chat", "manage"],
    default_active_agent="manage",
)

swarm = workflow.compile(checkpointer=checkpointer)
