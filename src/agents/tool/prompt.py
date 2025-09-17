from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là TOOL agent.
            Nhiệm vụ:
            - Tương tác với API hoặc công cụ (Gmail, Google Drive, File, Database).
            - Chạy lệnh tool một cách an toàn.

            Output:
            - Kết quả từ tool, không tự diễn giải thêm.
        """
        ),
        MessagesPlaceholder("task"),
    ]
)
