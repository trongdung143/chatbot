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
planner = PlannerAgent()
search = SearchAgent()
tool = ToolAgent()
vision = VisionAgent()
memory = MemoryAgent()


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


app.add_node("assigner", assigner.process)
app.add_node("analyst", analyst.process)
app.add_node("writer", writer.process)
app.add_node("supervisor", supervisor.process)
app.add_node("calculator", calculator.process)
app.add_node("coder", coder.process)
app.add_node("memory", memory.process)
app.add_node("planner", planner.process)
app.add_node("search", search.process)
app.add_node("tool", tool.process)
app.add_node("vision", vision.process)

app.set_entry_point("memory")
app.add_conditional_edges(
    "assigner",
    route,
    {
        "analyst": "analyst",
        "writer": "writer",
        "coder": "coder",
        "planner": "planner",
        "search": "search",
        "tool": "tool",
        "vision": "vision",
    },
)
app.add_conditional_edges(
    "supervisor",
    route,
    {"calculator": "calculator", "writer": "writer"},
)
app.add_edge("memory", "assigner")
app.add_edge("analyst", "supervisor")
app.add_edge("calculator", "writer")
app.add_edge("coder", "writer")
app.add_edge("planner", "writer")
app.add_edge("search", "writer")
app.add_edge("tool", "writer")
app.add_edge("vision", "writer")
app.set_finish_point("writer")


graph = app.compile(checkpointer=MemorySaver())
