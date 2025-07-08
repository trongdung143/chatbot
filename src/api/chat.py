from fastapi import APIRouter, Cookie, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional, AsyncGenerator
import json
from src.agents.workflow import graph
from langchain_core.messages import HumanMessage, SystemMessage, AIMessageChunk
from src.utils.handler import save_upload_file_into_temp

router = APIRouter()


async def generate_chat_stream(
        message: str,
        session_id: Optional[str],
        file: Optional[UploadFile] = None
) -> AsyncGenerator[str, None]:
    try:
        if file:
            save_upload_file_into_temp(file)

        input_state = {
            "messages": [
                SystemMessage(
                    "If the request exceeds your capabilities, automatically transfer to another agent that can handle it without asking the user (use transfer_to_<agent>)"
                ),
                SystemMessage("Always respond in Vietnamese"),
                SystemMessage("you have the ability to remember"),
                HumanMessage(content=message),
            ],
        }
        config = {"configurable": {"thread_id": session_id}}

        async for event in graph.astream(input_state, config=config, stream_mode="messages"):
            if isinstance(event, tuple) and len(event) >= 1:
                chunk, metadata = event[0], event[1] if len(event) > 1 else {}

                if isinstance(chunk, AIMessageChunk) and chunk.content:
                    data = {
                        "type": "chunk",
                        "content": chunk.content,
                        "node": metadata.get("langgraph_node", "unknown"),
                        "step": metadata.get("langgraph_step", 0)
                    }
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

        yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

    except Exception as e:
        error_data = {
            "type": "error",
            "message": str(e)
        }
        yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"


@router.post("/chat")
async def chatbot_stream(
        message: str = Form(...),
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
        }
    )
