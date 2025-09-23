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


prompt_supervisor = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là SUPERVISOR agent.

            Nhiệm vụ:
            - Đọc yêu cầu gốc của người dùng và kết quả phân tích từ agent vừa thực hiện.
            - Nếu phân tích còn thiếu, mơ hồ, sai sót thì viết feedback và đặt 'next_agent' là 'llm_node'
            - Nếu cần thêm thông tin từ người dùng thì đặt 'next_agent' là 'human_node' 
            - Nếu yêu cầu đã rõ ràng mà không cần phân tích lại hoặc thêm thông tin từ người dùng thì 'next_agent' là None
            """
        ),
        MessagesPlaceholder("supervision"),
    ]
)
