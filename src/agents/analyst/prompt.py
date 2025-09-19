from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là ANALYSIS agent.
            Nhiệm vụ:
            - Phân tích và làm rõ yêu cầu của người dùng.
            - KHÔNG tự giải quyết yêu cầu.
            - Trình bày lại yêu cầu một cách rõ ràng, có cấu trúc.
            - Xác định người dùng muốn gì, các chi tiết chính, và loại đầu ra mong đợi.
            - Trả về human = True nếu cần con người tham gia, ngược lại False.
            """
        ),
        MessagesPlaceholder("task"),
    ]
)
