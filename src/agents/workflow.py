from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import StateGraph
from src.agents.analyst.analyst import AnalystAgent
from src.agents.writer.writer import WriterAgent
from src.agents.assigner.assigner import AssignerAgent
from src.agents.state import State
from src.agents.calculator.calculator import CalculatorAgent
from src.agents.supervisor.supervisor import SupervisorAgent

app = StateGraph(State)

assginer = AssignerAgent()
analysis = AnalystAgent()
writer = WriterAgent()
calculator = CalculatorAgent()
supervisor = SupervisorAgent()


def route(state: State) -> str:
    if state.get("next_agent") in "analyst":
        return "analyst"
    elif state.get("next_agent") in "writer":
        return "writer"
    elif state.get("next_agent") in "calculator":
        return "calculator"


app.add_node("assigner", assginer.get_graph())
app.add_node("analyst", analysis.get_graph())
app.add_node("writer", writer.get_graph())
app.add_node("supervisor", supervisor.get_graph())
app.add_node("calculator", calculator.get_graph())

app.set_entry_point("assigner")
app.add_conditional_edges("assigner", route, {"analyst": "analyst", "writer": "writer"})
app.add_conditional_edges(
    "supervisor", route, {"calculator": "calculator", "writer": "writer"}
)
app.add_edge("analyst", "supervisor")
app.add_edge("calculator", "writer")
app.set_finish_point("writer")

graph = app.compile(checkpointer=MemorySaver())
