import fitz
import os
from src.agents.state import State
import shutil


def extract_text_from_pdf(state: State) -> str:
    save_dir = "src/data/temp"
    data_path = os.path.join(save_dir, state.get("thread_id"), state.get("file_path"))
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"PDF not found at: {data_path}")

    with fitz.open(data_path) as doc:
        text = "".join(page.get_text() for page in doc)
    shutil.rmtree(os.path.join(save_dir, state.get("thread_id")))
    return text
