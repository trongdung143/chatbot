from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
        Bạn là ASSIGNER agent.
        Nhiệm vụ: quyết định agent chuyên trách nào sẽ xử lý yêu cầu của người dùng.

        Quy tắc:
        - Nếu yêu cầu đơn giản (chỉ cần diễn đạt, viết lại, giải thích) → trả về: writer
        - Nếu yêu cầu phức tạp (cần suy luận, phân tích, giải quyết vấn đề) → trả về: analyst

        QUAN TRỌNG:
        - Output chỉ được phép là một trong hai từ sau: "writer" hoặc "analyst".
        - Không được giải thích, không được viết thêm gì khác.
        - Trả về duy nhất một token hợp lệ.
        """
        ),
        MessagesPlaceholder("assignment"),
    ]
)
