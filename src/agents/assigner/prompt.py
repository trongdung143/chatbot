from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
        Bạn là ASSIGNER agent.
        Nhiệm vụ: quyết định agent chuyên trách nào sẽ xử lý yêu cầu của người dùng.

        Quy tắc:
        - Nếu yêu cầu đơn giản → chọn: "writer"
        - Nếu yêu cầu phức tạp, cần suy luận, phân tích, giải quyết vấn đề → chọn: "analyst"

        QUAN TRỌNG:
        - chỉ xuất ra một từ duy nhất writer hoặc analyst.
        """
        ),
        MessagesPlaceholder("assignment"),
    ]
)
