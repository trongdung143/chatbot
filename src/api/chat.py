from fastapi import APIRouter, Cookie, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional, AsyncGenerator
import json
import time
from src.agents.workflow import graph
from langchain_core.messages import HumanMessage, AIMessage, RemoveMessage
from src.utils.handler import save_upload_file_into_temp
from langgraph.types import Command
from langgraph.graph.message import REMOVE_ALL_MESSAGES

router = APIRouter()


async def generate_chat_stream(
    message: str,
    conversation_id: str,
    file_path: Optional[str] = None,
    messages: Optional[list[dict]] = None,
) -> AsyncGenerator[str, None]:
    try:
        input_state = {
            "messages": [HumanMessage(content=message)],
            "thread_id": conversation_id,
            "next_agent": None,
            "prev_agent": None,
            "task": None,
            "result": None,
            "human": None,
            "file_path": file_path,
        }

        config = {"configurable": {"thread_id": conversation_id}}

        if messages:
            old_messages = []
            for msg in messages:
                if msg.get("sendertype") == "USER":
                    old_messages.append(HumanMessage(content=msg.get("content")))
                elif msg.get("sendertype") == "AI":
                    old_messages.append(AIMessage(content=msg.get("content")))
            graph.update_state(
                config=config,
                values={
                    "messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)] + old_messages
                },
            )

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
            node_subgraph, data_type, chunk = event
            if data_type == "updates":
                if chunk.get("__interrupt__") and not node_subgraph:
                    for interrupt in chunk["__interrupt__"]:
                        yield f"data: {json.dumps({'type': 'interrupt',
                                                    'response': interrupt.value.get("AIMessage")
                                                }, ensure_ascii=False)}\n\n"
            if data_type == "messages":
                response, meta = chunk
                agent = meta.get("langgraph_node", "unknown")

                yield f"data: {json.dumps({'type': 'chunk',
                                            'response': response.content,
                                            'agent': agent}, ensure_ascii=False)}\n\n"
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
    conversation_id: str = Cookie(None),
    messages: Optional[list[dict]] = Form(None),
) -> StreamingResponse:
    file_path = None
    if file:
        file_path = save_upload_file_into_temp(file, conversation_id)
    return StreamingResponse(
        generate_chat_stream(message, conversation_id, file_path, messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "X-Accel-Buffering": "no",
        },
    )
