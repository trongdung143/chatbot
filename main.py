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
