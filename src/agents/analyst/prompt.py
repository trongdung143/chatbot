from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
You are the ANALYSIS agent.
Your job: analyze and clarify the user's request.
- Do NOT solve the request.
- Restate the request clearly and in a structured way.
- Identify what the user wants, key details, and expected type of output.
"""
        ),
        MessagesPlaceholder("task"),
    ]
)
