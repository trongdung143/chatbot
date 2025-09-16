from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import StateGraph
from src.agents.analyst.analyst import AnalystAgent
from src.agents.writer.writer import WriterAgent
from src.agents.assigner.assigner import AssignerAgent
from src.agents.state import State
from src.agents.calculator.calculator import CalculatorAgent
from src.agents.supervisor.supervisor import SupervisorAgent
from src.agents.coder.coder import CoderAgent
from src.agents.memory.memory import MemoryAgent
from src.agents.planner.planner import PlannerAgent
from src.agents.search.search import SearchAgent
from src.agents.tool.tool import ToolAgent
from src.agents.vision.vision import VisionAgent

app = StateGraph(State)

assigner = AssignerAgent()
analyst = AnalystAgent()
writer = WriterAgent()
calculator = CalculatorAgent()
supervisor = SupervisorAgent()
coder = CoderAgent()
memory = MemoryAgent()
planner = PlannerAgent()
search = SearchAgent()
tool = ToolAgent()
vision = VisionAgent()


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
    ]
    if next_agent in VALID_AGENTS:
        return next_agent
    return "writer"


app.add_node("assigner", assigner.get_graph())
app.add_node("analyst", analyst.get_graph())
app.add_node("writer", writer.get_graph())
app.add_node("supervisor", supervisor.get_graph())
app.add_node("calculator", calculator.get_graph())
app.add_node("coder", coder.get_graph())
app.add_node("memory", memory.get_graph())
app.add_node("planner", planner.get_graph())
app.add_node("search", search.get_graph())
app.add_node("tool", tool.get_graph())
app.add_node("vision", vision.get_graph())

app.set_entry_point("assigner")
app.add_conditional_edges(
    "assigner",
    route,
    {
        "analyst": "analyst",
        "writer": "writer",
        "coder": "coder",
        "memory": "memory",
        "planner": "planner",
        "search": "search",
        "tool": "tool",
        "vision": "vision",
    },
)
app.add_conditional_edges(
    "supervisor",
    route,
    {"calculator": "calculator", "writer": "writer", "analyst": "analyst"},
)
app.add_edge("analyst", "supervisor")
app.add_edge("calculator", "writer")
app.add_edge("coder", "writer")
app.add_edge("memory", "writer")
app.add_edge("planner", "writer")
app.add_edge("search", "writer")
app.add_edge("tool", "writer")
app.add_edge("vision", "writer")
app.set_finish_point("writer")


graph = app.compile(checkpointer=MemorySaver())
