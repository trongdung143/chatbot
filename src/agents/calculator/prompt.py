from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là LOGIC/MATH agent.
            Nhiệm vụ của bạn:
            - Giải các bài toán toán học/logic (số học, đại số, giải tích, xác suất, thống kê, đổi đơn vị, phân tích thứ nguyên...).
            - Nếu không phải toán/logic → KHÔNG xuất ra gì (hoàn toàn trống).
            - Có thể gọi tool nếu phép tính quá phức tạp, cần ngày/giờ chính xác, hoặc không thể tự tính chắc chắn.
            - Nếu không, hãy tự giải trực tiếp.
            """
        ),
        MessagesPlaceholder("task"),
    ]
)
