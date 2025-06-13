from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.setup import GOOGLE_API_KEY
from langgraph.prebuilt import create_react_agent
from src.agents.prompts.prompts_read import read_prompt

# import tools
from src.agents.tools.tranfers import transfer_to_chat
from src.agents.tools.file import *
from src.agents.tools.system import *
from src.agents.tools.rag import *

tools = [
    transfer_to_chat,
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

# model = ChatOpenAI(
#     model="gpt-3.5-turbo",
#     openai_api_key=OPENAI_API_KEY,
#     cache=False,
#     streaming=True,
#     temperature=0,
# )

# model = Together(
#     model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
#     temperature=0.1,
#     top_p=0.9,
#     repetition_penalty=1.3,
#     max_tokens=512,
#     together_api_key=TOGETHER_API_KEY,
# )

agent = create_react_agent(
    model=model,
    tools=tools,
    name="manage",
    prompt=read_prompt("src/agents/prompts/prompts.txt"),
)
