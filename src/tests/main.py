import requests
from src.config.setup import GOOGLE_API_KEY, SEARCH_ENGINE_ID

query = "chatgpt là gì"

url = "https://www.googleapis.com/customsearch/v1"
params = {
    "key": GOOGLE_API_KEY,
    "cx": SEARCH_ENGINE_ID,
    "q": query,
    "num": 3,
}

response = requests.get(url, params=params)
data = response.json()

for item in data.get("items", []):
    print("Title:", item["title"])
    print("Link:", item["link"])
    print()
