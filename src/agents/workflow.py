from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import StateGraph
from src.agents.analyst.analyst import AnalystAgent
from src.agents.writer.writer import WriterAgent
from src.agents.assigner.assigner import AssignerAgent
from src.agents.state import State
from src.agents.calculator.calculator import CalculatorAgent

app = StateGraph(State)

supervisor = AssignerAgent()
analysis = AnalystAgent()
writer = WriterAgent()
logic = CalculatorAgent()


def route(state: State) -> str:
    if state["next_agent"] in "analyst":
        return "analyst"
    elif state["next_agent"] in "writer":
        return "writer"


app.add_node("assigner", supervisor.get_graph())
app.add_node("analyst", analysis.get_graph())
app.add_node("writer", writer.get_graph())

app.add_node("calculator", logic.get_graph())

app.set_entry_point("assigner")
app.add_conditional_edges("assigner", route, {"analyst": "analyst", "writer": "writer"})
app.add_edge("analyst", "calculator")
app.add_edge("calculator", "writer")
app.set_finish_point("writer")

graph = app.compile(checkpointer=MemorySaver())
