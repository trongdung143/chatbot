from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là RAG agent.
            Nhiệm vụ của bạn:
            
            """
        ),
        MessagesPlaceholder("task"),
    ]
)

prompt_supervisor =  ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là SUPERVISOR agent.
            Nhiệm vụ của bạn:
            
            """
        ),
        MessagesPlaceholder("task"),
    ]
)
