from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.setup import GOOGLE_API_KEY
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

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
    model=model, tools=[], name="chat", prompt="", checkpointer=MemorySaver()
)
