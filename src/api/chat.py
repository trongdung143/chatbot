from fastapi import APIRouter, Cookie, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional, AsyncGenerator
import json
from src.agents.workflow import graph
from langchain_core.messages import HumanMessage, SystemMessage, AIMessageChunk
from src.utils.handler import save_upload_file_into_temp
from langgraph.types import Command

router = APIRouter()


async def generate_chat_stream(
    message: str, session_id: Optional[str], file: Optional[UploadFile] = None
) -> AsyncGenerator[str, None]:
    try:
        if file:
            save_upload_file_into_temp(file)

        input_state = {
            "messages": [HumanMessage(content=message)],
            "thread_id": session_id,
            "next_agent": None,
            "prev_agent": None,
            "task": None,
            "result": None,
            "human": None,
        }

        config = {"configurable": {"thread_id": session_id}}

        interrupt = graph.get_state(config=config).interrupts
        if interrupt:
            input_state = {
                "messages": [HumanMessage(content=message)],
            }
            input_state = Command(resume=message)
        async for event in graph.astream(
            input=input_state,
            config=config,
            stream_mode=["messages", "updates"],
            subgraphs=True,
        ):
            _, data_type, chunk = event

            if data_type == "update":
                pass
            if data_type == "messages":
                msg, meta = chunk
                agent = meta.get("langgraph_node", "unknown")
                if agent not in [
                    "memory",
                    "supervisor",
                    "assigner",
                ]:  # not in ["writer", "analyst"]:
                    # continue
                    yield f"data: {json.dumps({'type': 'chunk', 'content': msg.content}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"

    except Exception as e:
        error_data = {"type": "error", "message": str(e)}
        yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"


@router.post("/chat")
async def chatbot_stream(
    message: str = Form(""),
    file: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Cookie(None),
) -> StreamingResponse:
    return StreamingResponse(
        generate_chat_stream(message, session_id, file),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "X-Accel-Buffering": "no",
        },
    )
