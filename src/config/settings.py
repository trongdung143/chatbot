from dotenv import load_dotenv
import os
import redis.asyncio as redis
import json

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
PASSWORD = os.getenv("PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = os.getenv("TOKEN_URL")
USERINFO_URL = os.getenv("USERINFO_URL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SCOPE = "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.compose https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/gmail.labels https://www.googleapis.com/auth/gmail.settings.basic https://www.googleapis.com/auth/gmail.settings.sharing https://www.googleapis.com/auth/documents https://www.googleapis.com/auth/presentations https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/forms.body https://www.googleapis.com/auth/forms.responses.readonly https://www.googleapis.com/auth/photoslibrary.readonly https://www.googleapis.com/auth/calendar openid email profile"

try:
    with open("src/config/supported_apps.json", "r", encoding="utf-8") as f:
        SUPPORTED_APPS = json.load(f)
except Exception as e:
    SUPPORTED_APPS = {}
    print(f"Error loading supported_apps.json: {e}")
