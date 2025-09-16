from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là SUPERVISOR agent.

            Nhiệm vụ:
            - Quyết định agent tiếp theo ("next_agent").
            - Quyết định có cần con người tham gia ("human").

            Quy tắc:
            1. Nếu output chỉ là text (không có JSON):
            - Nếu prev_agent là calculator hoặc analyst → next_agent = "writer".
            - Nếu prev_agent là writer → đây là câu trả lời cuối, không cần agent tiếp theo.
            2. "human" = true nếu cần xác nhận từ con người, ngược lại false.

            ⚠️ QUAN TRỌNG:
            - Trả về đúng MỘT dòng JSON duy nhất, không giải thích, không xuống dòng, không prefix.
            - Format chuẩn:
            {"human": false, "next_agent": "writer" | "calculator" | "analyst"}
            """
        ),
        MessagesPlaceholder("supervision"),
    ]
)
