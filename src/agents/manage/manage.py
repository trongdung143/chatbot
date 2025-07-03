from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Literal
from src.agents.state import State

from langgraph.types import interrupt, Command
# import tools
from src.tools.tranfers import transfer_to_chat
from src.tools.life import *
from src.prompts.prompts_read import read_prompt
from src.tools.file import *
from src.tools.system import *
from src.tools.rag import *

tools = [
    transfer_to_chat,
    get_time,
    get_weather,
    rag_web,
    get_relative_date,
    save_upload_file,
    show_saved_file_folder,
    remove_file,
    write_note,
    read_note,
    get_system_info,
    rename_file,
    restart_server,
    open_application,
    close_application,
    shutdown_system,
    restart_system,
    download_file,
    rag_file,
]

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    disable_streaming=False,
).bind_tools(tools)


async def manage(state: State):
    return {"messages": [await model.ainvoke(state["messages"])]}


graph = StateGraph(State)
graph.add_node("manage", manage)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("manage")
graph.add_conditional_edges("manage", tools_condition)
graph.add_edge("tools", "manage")

agent = graph.compile(name="manage")
