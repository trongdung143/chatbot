from typing import Sequence

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.tools.base import BaseTool
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel

from src.agents.base import BaseAgent
from src.agents.rag.prompt import prompt, prompt_supervisor
from src.agents.state import State
from src.agents.supervisor.supervisor import SupervisorAgent
from src.config.setup import GOOGLE_API_KEY


class RagState(dict):
    task: str
    result: str
    next_node: str
    prev_node: str
    conversation_id: str
    document_path: str
    vectorstore_path: str
    retriever: list[str] | None = None

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
    VALID_NODES = [
        "re_question",
        "genarate",
        "__end__"
    ]
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="rag",
            tools=tools,
            state=RagState,
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

        self._retriever = None

        self._supervisor = SupervisorForRag()

        self._embedding = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY,
        )

        self._set_subgraph()

    def _route(self, state: RagState) -> str:
        next_node = state.get("next_node").strip()
        if next_node in self.VALID_NODES:
            return next_node
        return "__end__"

    def _set_subgraph(self):
        self._sub_graph.add_node("supervisor", self._supervisor.process)
        self._sub_graph.add_node("docs_to_vec", self._document_to_vector)
        self._sub_graph.add_node("retrieve", self._retrieve)
        self._sub_graph.add_node("reviewer", self._reviewer)
        self._sub_graph.add_node("genarate", self._genarate)
        self._sub_graph.add_node("re_question", self._re_question)


        self._sub_graph.set_entry_point("docs_to_vec")

        self._sub_graph.add_edge("docs_to_vec", "retrieve")
        self._sub_graph.add_edge("retrieve", "reviewer")

        self._sub_graph.add_conditional_edges(
            "reviewer",
            self._route,
            {
                "re_question": "re_question",
                "genarate": "genarate",
            }
        )

        self._sub_graph.add_edge("re_question", "retrieve")
        self._sub_graph.add_edge("genarate", "supervisor")

        self._sub_graph.add_conditional_edges(
            "supervisor",
            self._route,
            {
                "__end__" : "__end__",
                "genarate" : "genarate",
            }
        )



    async def _document_to_vector(self, state: RagState) -> RagState:
        document_path = state.get("document_path")
        vector_store_path = state.get("vector_store_path")

        loader = PyPDFLoader(document_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=500, chunk_overlap=100)
        documents_splits = text_splitter.split_documents(documents)

        # vectorstore = await Chroma.afrom_documents(
        #     documents=documents_splits,
        #     collection_name=vector_store_path,
        #     embedding=self._embedding,
        #     persist_directory=vector_store_path,
        # )
        #
        # vectorstore.persist()

        vectorstore = await FAISS.afrom_documents(
            documents=documents_splits,
            embedding=self._embedding,
        )

        vectorstore.save_local(vector_store_path)

        retriever = vectorstore.as_retriever()

        self._retriever = retriever
        return state

    async def _retrieve(self, state: RagState) -> RagState:
        task = state.get("task")
        response = self._retriever.ainvoke(task)
        retriever = [doc.page_content for doc in response]
        state.update(retriever=retriever)
        return state

    async def _reviewer(self, state: RagState) -> RagState:

        return state

    async def _genarate(self, state: RagState) -> RagState:
        return state

    async def _re_question(self, state: RagState) -> RagState:
        return state

    async def process(self, state: State) -> State:
        input_state = {

        }
        sub_graph = self.get_subgraph()
        response = await sub_graph.ainvoke(input=input_state)
        state.update()
        return state
