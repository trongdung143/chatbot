from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            Bạn là PLANNER agent.
            Nhiệm vụ:
            - Lập kế hoạch nhiều bước để giải quyết một yêu cầu phức tạp.
            - Chia task thành subtask, gợi ý agent nào nên xử lý từng bước.
            Output:
            - Danh sách các bước, mỗi bước gắn agent phù hợp.
        """
        ),
        MessagesPlaceholder("task"),
    ]
)
