from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.setup import GOOGLE_API_KEY
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# import tools
# from src.agents.tools.tranfers import transfer_to_manage
from src.agents.tools.life import *
from src.agents.tools.rag import *
from src.agents.tools.google import *
from src.agents.tools.file import *
from src.agents.tools.system import *
from src.agents.tools.rag import *
from src.agents.prompts.prompts_read import *

tools = [
    # transfer_to_manage,
    get_time,
    get_weather,
    rag_web,
    send_email,
    get_received_emails_by_date,
    get_sent_emails_by_date,
    get_relative_date,
    list_drive_files,
    delete_drive_file,
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
    disable_streaming=True,
)

checkpointer = MemorySaver()
agent = create_react_agent(
    model=model,
    tools=tools,
    name="chat",
    checkpointer=checkpointer,
    prompt=read_prompt("src/agents/prompts/prompts.txt"),
)
