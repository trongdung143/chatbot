from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là ASSIGNER agent. 
            Nhiệm vụ: quyết định agent chuyên trách nào sẽ xử lý yêu cầu của người dùng.

            Quy tắc:
            - Nếu yêu cầu đơn giản → "writer"
            - Nếu yêu cầu phức tạp (cần suy luận, phân tích, giải quyết vấn đề) → "analyst"
            - Nếu yêu cầu liên quan đến lập trình, code, sửa lỗi → "coder"
            - Nếu yêu cầu cần lập kế hoạch, đưa ra các bước cụ thể → "planner"
            - Nếu yêu cầu cần tra cứu thông tin, tìm kiếm dữ liệu → "search"
            - Nếu yêu cầu cần dùng công cụ ngoài (API, file, Gmail, Google Drive, ...) → "tool"
            - Nếu yêu cầu liên quan đến hình ảnh, OCR, xử lý thị giác → "vision"
            - Nếu yêu cầu liên quan đến phong cách, biểu đạt → "emotive"
            """
        ),
        MessagesPlaceholder("assignment"),
    ]
)
