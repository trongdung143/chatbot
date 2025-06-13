import json
import httpx
import base64
from email.mime.text import MIMEText
from langchain_core.tools import tool
from src.config.setup import *
from datetime import datetime, timedelta


async def get_access_token(session_id: str) -> str:
    if not session_id:
        return None

    session_json = await redis_client.get(f"session:{session_id}")
    if not session_json:
        return None

    session_data = json.loads(session_json)
    access_token = session_data.get("access_token")
    expires_at = session_data.get("expires_at")
    refresh_token = session_data.get("refresh_token")

    if expires_at and datetime.utcnow() >= datetime.fromisoformat(expires_at):
        if not refresh_token:
            return None

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                        "refresh_token": refresh_token,
                        "grant_type": "refresh_token",
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                resp.raise_for_status()
                token_data = resp.json()
                new_access_token = token_data["access_token"]
                expires_in = token_data["expires_in"]

                session_data["access_token"] = new_access_token
                session_data["expires_at"] = (
                    datetime.utcnow() + timedelta(seconds=expires_in)
                ).isoformat()

                await redis_client.set(
                    f"session:{session_id}",
                    json.dumps(session_data),
                    ex=expires_in,
                )

                return new_access_token
        except Exception as e:
            return None
    else:
        return access_token


# ==================== GMAIL TOOLS ====================


@tool
async def send_email(to: str, subject: str, body: str, session_id: str) -> str:
    """
    Send an email via the Gmail API with the provided content.

    Args:
        to (str): Recipient email address.
        subject (str): Email subject.
        body (str): Email body in plain text.
        session_id (str): saved in the chat history of the chat with you.

    Returns:
        str: A JSON string containing the Gmail API response or error.
    """
    try:
        access_token = await get_access_token(session_id)
        if not access_token:
            return json.dumps({"error": "No access token found"})

        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        data = {"raw": raw_message}

        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data)
            resp.raise_for_status()
            return "sent successfully"

    except httpx.HTTPStatusError as e:
        error_message = e.response.json()
        return json.dumps(
            {
                "error": "Failed to send email",
                "status_code": e.response.status_code,
                "details": error_message,
            }
        )
    except Exception as e:
        return "An unexpected error occurred"


@tool
async def get_sent_emails_by_date(session_id: str, after: str, before: str) -> str:
    """
    Fetch the subject lines of sent emails from Gmail within a given date range.

    Args:
        session_id (str): saved in the chat history of the chat with you.
        after (str): Start date in the format yyyy/mm/dd.
        before (str): End date in the format yyyy/mm/dd.

    Returns:
        str: The subject of the email sent during the specified time period and the ID corresponding to that email.
    """
    access_token = await get_access_token(session_id)
    if not access_token:
        return "No access token found"

    query = f"in:sent after:{after} before:{before}"
    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages?q={query}"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        messages = resp.json().get("messages", [])

        if not messages:
            return "No sent emails found in the given date range."

        results = []
        for msg in messages:
            msg_id = msg["id"]
            detail_url = (
                f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}"
            )
            detail_resp = await client.get(detail_url, headers=headers)
            detail_resp.raise_for_status()
            msg_data = detail_resp.json()

            headers_list = msg_data.get("payload", {}).get("headers", [])
            subject = next(
                (h["value"] for h in headers_list if h["name"] == "Subject"),
                "(No Subject)",
            )
            results.append(subject + f" ID: {msg_id}")

        return "\n".join(results)


@tool
async def get_received_emails_by_date(session_id: str, after: str, before: str) -> str:
    """
    Fetch the subject lines of received emails from Gmail within a given date range.

    Args:
        session_id (str): saved in the chat history of the chat with you
        after (str): Start date in format yyyy/mm/dd.
        before (str): End date in format yyyy/mm/dd.

    Returns:
        str: email subjects received during the specified time period and the ID corresponding to that email.
    """
    access_token = await get_access_token(session_id)
    if not access_token:
        return "No access token found"

    query = f"in:inbox after:{after} before:{before}"
    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages?q={query}"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        messages = resp.json().get("messages", [])

        if not messages:
            return "No emails found in the given date range."

        subjects = []
        for msg in messages:
            msg_id = msg["id"]
            detail_url = (
                f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}"
            )
            detail_resp = await client.get(detail_url, headers=headers)
            detail_resp.raise_for_status()
            msg_data = detail_resp.json()

            headers_list = msg_data.get("payload", {}).get("headers", [])
            subject = next(
                (h["value"] for h in headers_list if h["name"] == "Subject"),
                "(No Subject)",
            )
            subjects.append(subject + f" ID: {msg_id}")
        return "\n".join(subjects)


# ==================== GOOGLE DRIVE TOOLS ====================


@tool
async def list_drive_files(
    session_id: str, folder_id: str = None, query: str = None
) -> str:
    """
    List files in Google Drive with optional filters and customizable output (should ask the user what information is needed in the output).

    Args:
        session_id (str): The session ID used to retrieve the access token.
        folder_id (str, optional): ID of the folder to list files from. If None, lists from the root directory.
        query (str, optional): A search query to filter files (e.g., "name contains 'report'").

    Returns:
        str: A list of matching files including details such as name, ID, MIME type, last modified time,
             size, and web view link. The displayed fields may be customized based on user preferences.
    """

    access_token = await get_access_token(session_id)
    if not access_token:
        return "No access token found."

    url = "https://www.googleapis.com/drive/v3/files"
    headers = {"Authorization": f"Bearer {access_token}"}

    params = {
        "fields": "files(id,name,mimeType,modifiedTime,size,webViewLink)",
        "pageSize": 100,
    }

    query_parts = []
    if folder_id:
        query_parts.append(f"'{folder_id}' in parents")
    if query:
        query_parts.append(query)

    if query_parts:
        params["q"] = " and ".join(query_parts)

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()

            files = data.get("files", [])
            if not files:
                return "No files found."

            results = []
            for file in files:
                file_info = (
                    f"Name: {file['name']}\n"
                    f"ID: {file['id']}\n"
                    f"Type: {file['mimeType']}\n"
                    f"Modified: {file.get('modifiedTime', 'Unknown')}\n"
                    f"Size: {file.get('size', 'Unknown')} bytes\n"
                    f"Link: {file.get('webViewLink', 'N/A')}\n"
                    f"---"
                )
                results.append(file_info)

            return "\n".join(results)

    except httpx.HTTPStatusError as e:
        return f"Failed to list files: {e.response.text}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


@tool
async def delete_drive_file(session_id: str, files_id: str) -> str:
    """
    Delete one or more files from Google Drive.

    Args:
        session_id (str): The session ID used to retrieve the access token.
        files_id (str): A single file ID or a space-separated string of multiple file IDs.

    Returns:
        str: Summary of deletion results (successes and failures).
    """
    access_token = await get_access_token(session_id)
    if not access_token:
        return "No access token found."

    success = []
    failed = []

    try:
        async with httpx.AsyncClient() as client:
            for file_id in files_id.strip().split():
                try:
                    resp = await client.delete(
                        f"https://www.googleapis.com/drive/v3/files/{file_id}",
                        headers={"Authorization": f"Bearer {access_token}"},
                    )
                    resp.raise_for_status()
                    success.append(file_id)
                except httpx.HTTPStatusError as e:
                    failed.append(f"{file_id} (HTTP error: {e.response.status_code})")
                except Exception as ex:
                    failed.append(f"{file_id} (error: {str(ex)})")

        result = []
        if success:
            result.append(f"Deleted: {", ".join(success)}")
        if failed:
            result.append(f"Failed: {", ".join(failed)}")

        return "\n".join(result) if result else "No file IDs were provided."

    except Exception as e:
        return f"Unexpected error: {str(e)}"
