from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import StateGraph
from src.agents.analysis import AnalysisAgent
from src.agents.writer import WriterAgent
from src.agents.supervisor import SupervisorAgent
from src.agents.state import State
from src.agents.logic import LogicAgent

app = StateGraph(State)

supervisor = SupervisorAgent()
analysis = AnalysisAgent()
writer = WriterAgent()
logic = LogicAgent()


def route(state: State) -> str:
    if state["next_agent"] in "analysis":
        return "analysis"
    elif state["next_agent"] in "writer":
        return "writer"


app.add_node("supervisor", supervisor.get_builder().compile())
app.add_node("analysis", analysis.get_builder().compile())
app.add_node("writer", writer.get_builder().compile())
app.add_node("logic", logic.get_builder().compile())

app.set_entry_point("supervisor")
app.add_conditional_edges(
    "supervisor", route, {"analysis": "analysis", "writer": "writer"}
)
app.add_edge("analysis", "logic")
app.add_edge("logic", "writer")
app.set_finish_point("writer")

graph = app.compile(checkpointer=MemorySaver())
