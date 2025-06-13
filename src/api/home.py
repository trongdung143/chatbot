from fastapi import APIRouter, Cookie
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Optional

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_home(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        return RedirectResponse(url="/login", status_code=302)
    with open("src/static/chat/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)


@router.get("/home", response_class=HTMLResponse)
async def get_home(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        return RedirectResponse(url="/login", status_code=302)
    with open("src/static/chat/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)
