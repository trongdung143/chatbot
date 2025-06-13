from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api import chat_routes, home_routes, download_routes, account_routes
from fastapi.responses import JSONResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
)

BLOCKED_KEYWORDS = ["wget", "chmod", "rm", ";", "curl", "tftp", "ftpget"]


@app.middleware("http")
async def block_malicious_requests(request: Request, call_next):
    try:
        raw_url = str(request.url)
        if any(
            keyword in raw_url.lower()
            for keyword in ["wget", "curl", "sh ", "rm ", "chmod"]
        ):
            return JSONResponse(
                status_code=403,
                content={"detail": "Request bị chặn vì nghi ngờ có hành vi nguy hiểm."},
            )
        response = await call_next(request)
        return response
    except Exception:
        return JSONResponse(status_code=500, content={"detail": "Lỗi máy chủ nội bộ."})


app.include_router(chat_routes.router)
app.include_router(home_routes.router)
app.include_router(download_routes.router)
app.include_router(account_routes.router)
