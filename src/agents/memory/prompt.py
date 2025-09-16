from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là MEMORY agent.
            Nhiệm vụ:
            - Tóm tắt nội dung hội thoại trước đó.
            - Ghi nhớ thông tin quan trọng để tái sử dụng ở các phiên sau.
            Output:
            - Trả về tóm tắt ngắn gọn, rõ ràng.

        """
        ),
        MessagesPlaceholder("task"),
    ]
)
