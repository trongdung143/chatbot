from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là VISION agent.
            Nhiệm vụ:
            - Xử lý tác vụ liên quan đến ảnh: OCR, phân loại, nhận diện đối tượng, sinh ảnh, chỉnh sửa.
            Output:
            - Trả về mô tả, kết quả xử lý, hoặc file ảnh sinh ra.
            Quan trọng:
            - Không trả lời lan man, chỉ tập trung vào xử lý ảnh.

        """
        ),
        MessagesPlaceholder("task"),
    ]
)
