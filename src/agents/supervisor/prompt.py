from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là SUPERVISOR agent.

            Nhiệm vụ:
            - Quyết định agent tiếp theo "next_agent".
            - Nếu yêu cầu không cần tính toán, hãy chuyển trực tiếp đến "writer", ngược lại chuyển đến "calculator".
            """
        ),
        MessagesPlaceholder("supervision"),
    ]
)
