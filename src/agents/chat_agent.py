from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import GOOGLE_API_KEY
from langgraph.prebuilt import create_react_agent

# import tools
from src.agents.tools.tranfers import transfer_to_manage
from src.agents.tools.life_tools import *
from src.agents.tools.rag_tools import *
from src.agents.prompts.prompts_read import *
from src.agents.tools.google_tools import *

tools = [
    transfer_to_manage,
    get_time,
    get_weather,
    rag_web,
    send_email,
    get_received_emails_by_date,
    get_sent_emails_by_date,
    get_relative_date,
    delete_email_by_id,
]

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    disable_streaming=True,
)

agent = create_react_agent(
    model=model,
    tools=tools,
    name="chat",
    prompt=read_prompt("src/agents/prompts/prompts.txt"),
)
