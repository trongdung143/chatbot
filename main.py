import asyncio
from src.agents.workflow import graph
from langchain_core.messages import HumanMessage

input_state = {
    "messages": [
        HumanMessage(content="đạo hàm là gì và ví dụ tính toán cụ thể"),
    ],
    "thread_id": "123",
    "agent_logs": [],
    "next_agent": None,
    "prev_agent": None,
    "task": "",
}
config = {"configurable": {"thread_id": "123"}}


async def a():
    async for mode_data in graph.astream(
        input_state,
        config=config,
        stream_mode=["messages", "updates"],
    ):
        mode, payload = mode_data

        if mode == "messages":
            msg, meta = payload
            print(msg.content)


if __name__ == "__main__":
    asyncio.run(a())


{
    "__interrupt__": (
        Interrupt(
            value={"text_to_revise": "original text"},
            resumable=True,
            ns=["human_node:83e3bce4-afd7-f1a6-4104-8a20f85f8b01"],
        ),
    )
}


(
    Interrupt(
        value={
            "AIMessage": "Chào bạn,\n\nBạn muốn tôi cung cấp các ví dụ về đạo hàm, nhưng để tôi hiểu rõ hơn, bạn có thể cho biết cụ thể hơn được không? Ví dụ:\n\n1.  **Bạn muốn loại ví dụ nào?**\n    *   Ví dụ về đạo hàm của các hàm số cơ bản (ví dụ: $x^n$, sin(x), cos(x), e^x, ln(x))?\n    *   Ví dụ về quy tắc tính đạo hàm (ví dụ: quy tắc tích, quy tắc thương, quy tắc chuỗi)?\n    *   Ví dụ về ứng dụng của đạo hàm (ví dụ: tìm cực trị, tìm khoảng đồng biến/nghịch biến, giải bài toán tối ưu)?\n    *   Ví dụ về đạo hàm cấp cao?\n\n2.  **Mức độ phức tạp bạn mong muốn là gì?**\n    *   Ví dụ đơn giản, dễ hiểu?\n    *   Ví dụ phức tạp hơn, đòi hỏi nhiều bước tính toán?\n\n3.  **Bạn có yêu cầu cụ thể nào khác không?**\n    *   Ví dụ có lời giải chi tiết?\n    *   Ví dụ có hình ảnh minh họa?\n\nViệc bạn cung cấp thêm thông tin sẽ giúp tôi đưa ra các ví dụ phù hợp nhất với nhu cầu của bạn."
        },
        resumable=True,
        ns=[
            "analyst:e718becb-6228-5517-b947-59f2400c2e59",
            "human_node:7b9c340f-c76e-c9a1-6641-230ba11935f7",
        ],
    ),
)
