# from langchain_google_genai import ChatGoogleGenerativeAI
# from src.config.setup import GOOGLE_API_KEY
# from langgraph.checkpoint.memory import MemorySaver
#
# model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=GOOGLE_API_KEY,
#     disable_streaming=True,
# )
#
# agent = create_react_agent(
#     model=model, tools=[], name="chat", prompt="", checkpointer=MemorySaver()
# )
