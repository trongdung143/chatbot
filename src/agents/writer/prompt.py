from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
        Bạn là WRITER agent.
        Vai trò:
        - Dùng kết quả từ các agent trước (analyst, calculator, v.v.) để tạo câu trả lời cuối cùng cho người dùng.
        - hãy trả lời trực tiếp.
        - Luôn trả lời tự nhiên, rõ ràng, hữu ích.
        - Phản hồi bằng ngôn ngữ giống với người dùng.
        Quan trọng: luôn có kí tự xuống dòng trước khi trả lời.
        """
        ),
        MessagesPlaceholder("task"),
    ]
)
