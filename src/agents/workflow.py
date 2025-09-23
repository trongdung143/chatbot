from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import StateGraph
from src.agents.analyst.analyst import AnalystAgent
from src.agents.writer.writer import WriterAgent
from src.agents.assigner.assigner import AssignerAgent
from src.agents.state import State
from src.agents.calculator.calculator import CalculatorAgent
from src.agents.coder.coder import CoderAgent
from src.agents.memory.memory import MemoryAgent
from src.agents.planner.planner import PlannerAgent
from src.agents.search.search import SearchAgent
from src.agents.emotive.emotive import emotiveAgent

app = StateGraph(State)

assigner = AssignerAgent()
analyst = AnalystAgent()
writer = WriterAgent()
calculator = CalculatorAgent()
coder = CoderAgent()
planner = PlannerAgent()
search = SearchAgent()
memory = MemoryAgent()
emotive = emotiveAgent()


def route(state: State) -> str:
    next_agent = state.get("next_agent")
    VALID_AGENTS = [
        "analyst",
        "writer",
        "calculator",
        "coder",
        "memory",
        "planner",
        "search",
        "tool",
        "vision",
        "emotive",
    ]
    if next_agent in VALID_AGENTS:
        return next_agent
    return "writer"


app.add_node("assigner", assigner.process)
app.add_node("analyst", analyst.process)
app.add_node("writer", writer.process)
app.add_node("calculator", calculator.process)
app.add_node("coder", coder.process)
app.add_node("memory", memory.process)
app.add_node("planner", planner.process)
app.add_node("search", search.process)
app.add_node("emotive", emotive.process)

app.set_entry_point("memory")
app.add_edge("memory", "analyst")
app.add_edge("analyst", "assigner")
app.add_conditional_edges(
    "assigner",
    route,
    {
        "writer": "writer",
        "coder": "coder",
        "planner": "planner",
        "search": "search",
        "emotive": "emotive",
        "calculator": "calculator",
    },
)
app.add_edge("calculator", "writer")
app.add_edge("coder", "writer")
app.add_edge("planner", "writer")
app.add_edge("search", "writer")
app.add_edge("emotive", "__end__")
app.set_finish_point("writer")

graph = app.compile(checkpointer=MemorySaver())
