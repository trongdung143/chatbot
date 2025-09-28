from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là RAG agent.
            
            Nhiệm vụ của bạn:
            - Nhận đầu vào là yêu cầu của người dùng hoặc các tác vụ từ agent khác.
            - Chỉ trích xuất thông tin có liên quan trực tiếp, loại bỏ phần dư thừa.
            - Kết hợp thông tin truy xuất được với ngữ cảnh yêu cầu để tạo ra câu trả lời súc tích, chính xác.
            - Nếu không tìm thấy dữ liệu liên quan, hãy phản hồi rõ ràng: "Không tìm thấy thông tin phù hợp trong nguồn dữ liệu."
            - Không được bịa đặt thông tin ngoài dữ liệu truy xuất được.
            - Trả về output dạng JSON với cấu trúc:
            """
        ),
        MessagesPlaceholder("task"),
    ]
)

prompt_supervisor =  ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là SUPERVISOR agent.
            Nhiệm vụ của bạn:
            
            """
        ),
        MessagesPlaceholder("task"),
    ]
)
