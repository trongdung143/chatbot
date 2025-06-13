import fitz
import os
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup
import re
from tavily.async_tavily import AsyncTavilyClient
from src.config.setup import TAVILY_API_KEY
import asyncio
import tiktoken


def count_tokens(text, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


def extract_text_from_pdf(data_path: str) -> str:
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"PDF not found at: {data_path}")

    with fitz.open(data_path) as doc:
        text = "".join(page.get_text() for page in doc)

    return text


async def get_content_web_by_query(query: str) -> str:
    client = AsyncTavilyClient(TAVILY_API_KEY)
    response = await client.search(
        query=query, max_results=2, include_raw_content="text"
    )
    return response["results"]


def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main_content = soup.find("article", class_="md-content__inner")
    content = main_content.get_text() if main_content else soup.get_text()
    content = re.sub(r"\n\n+", "\n\n", content).strip()
    return content


async def get_content_web_by_url(url: str):
    loader = RecursiveUrlLoader(
        url,
        max_depth=5,
        extractor=bs4_extractor,
    )
    docs = await asyncio.to_thread(loader.load)
    return docs
