import os
from typing import Sequence

import fitz
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage
from langchain_core.tools.base import BaseTool
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel

from src.agents.base import BaseAgent
from src.agents.rag.prompt import prompt, prompt_supervisor
from src.agents.state import State
from src.config.setup import GOOGLE_API_KEY
from src.agents.supervisor.supervisor import SupervisorAgent

class RagState(State):
    conversation_id: str
    document_path: str
    vector_store_path: str
    web_search: str | None = None

class SupervisorResponseFormatForRag(BaseModel):
    pass

class SupervisorForRag(SupervisorAgent):
    def __init__(self):
        super().__init__(state=RagState, prompt=prompt_supervisor, response_format=SupervisorResponseFormatForRag)

    async def process(self, state: RagState) -> RagState:
        try:
            print("supervisor_node in rag agent")
        except Exception as e:
            print("ERROR ", "supervisor_node in rag agent\n", e)
        return state

class RagAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="rag",
            tools=tools,
            state=RagState,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

        self._embedding = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY,
        )

        # self._web_search_tool = TavilySearchResults(k=3)

    def _set_subgraph(self):
        pass


    async def _document_to_vector(self, state: RagState) -> RagState:
        document_path = state.get("document_path")
        vector_store_path = state.get("vector_store_path")

        loader = PyPDFLoader(document_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=500, chunk_overlap=100)
        documents_splits = text_splitter.split_documents(documents)
        vectorstore = await Chroma.afrom_documents(
            documents=documents_splits,
            collection_name="rag-chroma",
            embedding=self._embedding,
            persist_directory=vector_store_path,
        )
        vectorstore.persist()
        retriever = vectorstore.as_retriever()

        return state

    async def process(self, state: State) -> State:
        tasks = state.get("assigned_agents").get(self._agent_name)
        task = ""
        for t in tasks:
            task = task + f"{t}\n"
        result = None
        response = await self._chain.ainvoke({"task": [HumanMessage(content=task)]})
        result = f"[Kết quả tính toán] {response.content}"
        print("rag")
        current_tasks = state.get("tasks", {})
        current_results = state.get("results", {})

        current_tasks.setdefault(self._agent_name, []).append(task)

        current_results.setdefault(self._agent_name, []).append(result)
        state.update(
            human=False,
            prev_agent=self._agent_name,
            tasks=current_tasks,
            results=current_results,
        )
        return state
