from langgraph_swarm import create_handoff_tool

AGENTS = {"chat", "manage", "analysis", "search", "planner", "summarizer"}

handoff_tools = {
    name: create_handoff_tool(
        agent_name=name,
        description=f"Pass the task to the {name} agent",
    )
    for name in AGENTS
}

transfer_to_chat = handoff_tools["chat"]
transfer_to_manage = handoff_tools["manage"]
transfer_to_analysis = handoff_tools["analysis"]
transfer_to_search = handoff_tools["search"]
transfer_to_planner = handoff_tools["planner"]
transfer_to_summarizer = handoff_tools["summarizer"]
