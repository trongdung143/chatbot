from fastapi import APIRouter, Cookie, UploadFile, File, Form
from typing import Optional
from src.agents.base import swarm
from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.file_handler import save_upload_file_into_temp
import json
import redis.asyncio as redis

router = APIRouter()
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


async def get_access_token(session_id: Optional[str]) -> Optional[str]:
    if not session_id:
        return None
    session_json = await redis_client.get(f"session:{session_id}")
    if not session_json:
        return None
    session_data = json.loads(session_json)
    return session_data.get("access_token")


@router.post("/chat")
async def chatbot(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Cookie(None),
) -> dict:

    if file:
        save_upload_file_into_temp(file)
    input_state = {
        "messages": [
            SystemMessage(
                "If the request exceeds your capabilities, automatically transfer to another agent that can handle it without asking the user (use transfer_to_<agent>)"
            ),
            SystemMessage("Always respond in Vietnamese"),
            SystemMessage(f"session_id: {session_id}"),
            HumanMessage(content=message),
        ],
    }
    config = {"configurable": {"thread_id": session_id}}
    result = await swarm.ainvoke(input_state, config=config, stream_mode="values")
    return {"response": result["messages"][-1].content}
