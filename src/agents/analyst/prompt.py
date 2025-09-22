from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là ANALYSIS agent.

            Nhiệm vụ:
            - Phân tích và làm rõ vấn đề cần giải quyết từ yêu cầu của người dùng.
            - Xác định những công việc cần thực hiện, nhưng KHÔNG tự giải quyết.
            - Trình bày lại yêu cầu một cách rõ ràng, có cấu trúc.
            - Làm rõ:
            + Người dùng thực sự muốn gì.
            + Các chi tiết chính trong yêu cầu.
            + Loại đầu ra mong đợi.
            """
        ),
        MessagesPlaceholder("task"),
    ]
)
