from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from urllib.parse import urlencode
import httpx
import uuid
import logging
import json
from datetime import datetime, timedelta
from src.config.settings import *

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login():
    try:
        with open("src/static/account/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        logger.error("Login HTML file not found")
        raise HTTPException(status_code=404, detail="Login page not found")


@router.get("/login/google")
async def login_google():
    state = str(uuid.uuid4())
    # TODO:
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": SCOPE,
        "redirect_uri": REDIRECT_URI,
        "access_type": "offline",
        "prompt": "select_account",
        "state": state,
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url=auth_url)


@router.get("/login/google/callback")
async def login_google_callback(code: str = None, state: str = None, error: str = None):
    try:
        if error:
            logger.error(f"OAuth error: {error}")
            return RedirectResponse(url="/login?error=oauth_error")

        if not code:
            logger.error("No authorization code received")
            return RedirectResponse(url="/login?error=no_code")

        # TODO: Verify state với Redis (chống CSRF)
        logger.info(f"Received OAuth code: {code}, state: {state}")

        try:
            async with httpx.AsyncClient() as client:
                token_data = {
                    "code": code,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uri": REDIRECT_URI,
                    "grant_type": "authorization_code",
                }

                logger.info("Requesting access token...")
                token_resp = await client.post(TOKEN_URL, data=token_data)
                logger.info(f"Token response status: {token_resp.status_code}")
                token_resp.raise_for_status()
                token_result = token_resp.json()
                logger.info(f"Token response data: {token_result}")

                if "error" in token_result:
                    logger.error(f"Token exchange error: {token_result}")
                    return RedirectResponse(url="/login?error=token_error")

                access_token = token_result.get("access_token")
                refresh_token = token_result.get("refresh_token")
                id_token = token_result.get("id_token")
                expires_in = token_result.get("expires_in", 3600)

                if not access_token:
                    logger.error("No access token received")
                    return RedirectResponse(url="/login?error=no_token")

                headers = {"Authorization": f"Bearer {access_token}"}
                logger.info("Fetching user info...")
                userinfo_resp = await client.get(USERINFO_URL, headers=headers)
                logger.info(f"Userinfo response status: {userinfo_resp.status_code}")
                userinfo_resp.raise_for_status()
                userinfo = userinfo_resp.json()
                logger.info(f"User info: {userinfo}")

                if not userinfo.get("email"):
                    logger.error("No email in user info")
                    return RedirectResponse(url="/login?error=no_email")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during OAuth: {e}")
            return RedirectResponse(url="/login?error=http_error")
        except httpx.RequestError as e:
            logger.error(f"Request error during OAuth: {e}")
            return RedirectResponse(url="/login?error=request_error")
        except Exception as e:
            logger.error(f"Unexpected error during OAuth: {e}")
            return RedirectResponse(url="/login?error=unexpected_error")

        session_id = str(uuid.uuid4())
        logger.info(f"Generated session_id: {session_id}")

        session_data = {
            "user_id": userinfo.get("sub"),
            "email": userinfo.get("email"),
            "name": userinfo.get("name"),
            "picture": userinfo.get("picture"),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "id_token": id_token,
            "expires_at": (
                datetime.utcnow() + timedelta(seconds=expires_in)
            ).isoformat(),
            "created_at": datetime.utcnow().isoformat(),
        }

        logger.info(f"Saving session to Redis with key: session:{session_id}")
        await redis_client.set(
            f"session:{session_id}", json.dumps(session_data), ex=expires_in
        )

        logger.info(f"User {userinfo.get('email')} logged in successfully")

        response = RedirectResponse(url="/home")
        response.set_cookie(
            key="session_id",
            value=session_id,
            max_age=86400,
            httponly=True,
            samesite="lax",
            secure=True,
            path="/",
        )
        return response
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return "error"


@router.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        await redis_client.delete(f"session:{session_id}")

    response = RedirectResponse(url="/login")
    response.delete_cookie("session_id", path="/")
    return response
