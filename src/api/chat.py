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
            "agent_logs": [],
            "next_agent": None,
            "prev_agent": None,
            "task": None,
            "human": None,
        }

        config = {"configurable": {"thread_id": session_id}}

        interrupt = graph.get_state(config=config).interrupts
        if interrupt:
            input_state = Command(resume=message)
        async for event in graph.astream(
            input=input_state,
            config=config,
            stream_mode=["messages", "updates"],
            subgraphs=False,
        ):
            data_type, payload = event
            if data_type == "updates":
                type, state_data = next(reversed(payload.items()))

                if type == "__interrupt__":
                    continue
                    # yield f"data: {json.dumps({'type': 'chunk', 'content':state_data[0].value["AIMessage"]}, ensure_ascii=False)}\n\n"

                last_log = state_data["agent_logs"][-1]
                agent_name = last_log["agent_name"]
                duration = last_log["duration"]
                if agent_name != "assigner":
                    yield f"data: {json.dumps({'type': 'chunk', 'content': f'\n✅{agent_name}   **{duration:.2f}s**\n'}, ensure_ascii=False)}\n\n"
                # if not logs:
                #     logs.append(payload)
                # else:
                #     last = list(logs[-1].values())[0]["agent_logs"]
                #     current = list(payload.values())[0]["agent_logs"]
                #     if last != current:
                #         logs.append(payload)

            elif data_type == "messages":
                msg, meta = payload
                agent = meta.get("langgraph_node", "unknown")
                if agent == "assigner" or agent == "supervisor":
                    continue
                yield f"data: {json.dumps({'type': 'chunk', 'content': msg.content}, ensure_ascii=False)}\n\n"

            elif data_type == "error":
                yield f"data: {json.dumps({'type': 'error', 'message': str(payload)}, ensure_ascii=False)}\n\n"

        # for state in logs:
        #     for key in state:
        #         current_state = state[key]
        #         for log in current_state.get("agent_logs", []):
        #             name = log.get("agent_name")
        #             duration = log.get("duration")
        #             if name and duration is not None:
        #                 yield f"data: {json.dumps({'type': 'chunk', 'content': f'\n\n**{name.upper()}**   {duration:.2f}s'}, ensure_ascii=False)}\n\n"

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
