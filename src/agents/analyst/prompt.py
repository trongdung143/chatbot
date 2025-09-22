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
            - Đọc yêu cầu gốc của người dùng và kết quả từ agent vừa thực hiện.
            - Đánh giá xem agent vừa rồi đã hoàn thành công việc tốt chưa.
            - Nếu output còn thiếu, mơ hồ, sai sót → viết feedback và đặt 'next_agent' = agent, 'human' = False
            - Nếu output đã đủ và cần tính toán → 'next_agent' = "calculator", 'human' = False
            - Nếu output đã đủ và không cần tính toán → 'next_agent' = "writer" 'human' = False
            - Nếu không thể tự động quyết định → đặt 'human' = True, ngược lại là False
              Khi 'human' = True thì 'next_agent' cũng phải là "writer" hoặc "calculator" tùy theo loại yêu cầu.
            - Nếu output đã phân tích lại rồi thì trả về 'next_agent' tùy theo loại yêu cầu và 'human' là False.
            """
        ),
        MessagesPlaceholder("supervision"),
    ]
)
