# from typing import Sequence
# from langchain_core.tools.base import BaseTool
# from time import time
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.tools.base import BaseTool
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from src.agents.base import BaseAgent
# from src.agents.state import State
# from src.agents.calculator.prompt import prompt
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain.schema import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import Chroma
# from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
# from src.config.setup import GOOGLE_API_KEY
# import os
# import shutil
# import fitz
# from langchain_community.document_loaders import PyPDFLoader
#
# class RagState(State):
#     web_search: str | None = None
#     documents: list[str] | None = None
#
# class RagAgent(BaseAgent):
#     def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
#         super().__init__(
#             agent_name="rag",
#             tools=tools,
#             state=RagState,
#             model=None,
#         )
#
#         self._prompt = prompt
#
#         self._chain = self._prompt | self._model
#
#         self.web_search_tool = TavilySearchResults(k=3)
#
#     def _set_subgraph(self):
#         pass
#
#     def _extract_text_from_pdf(self, state: State) -> str:
#         save_dir = "src/data/temp"
#         data_path = os.path.join(save_dir, state.get("thread_id"), state.get("file_path"))
#         if not os.path.exists(data_path):
#             raise FileNotFoundError(f"PDF not found at: {data_path}")
#
#         with fitz.open(data_path) as doc:
#             text = "".join(page.get_text() for page in doc)
#
#         text_splitter = CharacterTextSplitter(
#             chunk_size=500, chunk_overlap=100, length_function=len, separator="\n"
#         )
#
#         texts = text_splitter.split_text(text)
#         state.up
#         print("extracting text from pdf")
#         return
#
#
#     def retrieve(self, state):
#         text_splitter = CharacterTextSplitter(
#             chunk_size=500, chunk_overlap=100, length_function=len, separator="\n"
#         )
#
#
#         # Add to vectorDB
#         vectorstore = Chroma.from_texts(
#             texts=,
#             collection_name="rag-chroma",
#             embedding=GoogleGenerativeAIEmbeddings(
#                 google_api_key=GOOGLE_API_KEY,
#                 model="gemini-embedding-001",
#             ),
#         )
#         retriever = vectorstore.as_retriever()
#         # Retrieval
#         documents = retriever.invoke(question)
#         return {"documents": documents, "question": question}
#
#     def generate(state):
#         """
#         Generate answer
#
#         Args:
#             state (dict): The current graph state
#
#         Returns:
#             state (dict): New key added to state, generation, that contains LLM generation
#         """
#         print("---GENERATE---")
#         question = state["question"]
#         documents = state["documents"]
#
#         # RAG generation
#         generation = rag_chain.invoke({"context": documents, "question": question})
#         return {"documents": documents, "question": question, "generation": generation}
#
#     def grade_documents(state):
#         """
#         Determines whether the retrieved documents are relevant to the question.
#
#         Args:
#             state (dict): The current graph state
#
#         Returns:
#             state (dict): Updates documents key with only filtered relevant documents
#         """
#
#         print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
#         question = state["question"]
#         documents = state["documents"]
#
#         # Score each doc
#         filtered_docs = []
#         web_search = "No"
#         for d in documents:
#             score = retrieval_grader.invoke(
#                 {"question": question, "document": d.page_content}
#             )
#             grade = score.binary_score
#             if grade == "yes":
#                 print("---GRADE: DOCUMENT RELEVANT---")
#                 filtered_docs.append(d)
#             else:
#                 print("---GRADE: DOCUMENT NOT RELEVANT---")
#                 web_search = "Yes"
#                 continue
#         return {"documents": filtered_docs, "question": question, "web_search": web_search}
#
#     def transform_query(state):
#         """
#         Transform the query to produce a better question.
#
#         Args:
#             state (dict): The current graph state
#
#         Returns:
#             state (dict): Updates question key with a re-phrased question
#         """
#
#         print("---TRANSFORM QUERY---")
#         question = state["question"]
#         documents = state["documents"]
#
#         # Re-write question
#         better_question = question_rewriter.invoke({"question": question})
#         return {"documents": documents, "question": better_question}
#
#     def web_search(state):
#         """
#         Web search based on the re-phrased question.
#
#         Args:
#             state (dict): The current graph state
#
#         Returns:
#             state (dict): Updates documents key with appended web results
#         """
#
#         print("---WEB SEARCH---")
#         question = state["question"]
#         documents = state["documents"]
#
#         # Web search
#         docs = web_search_tool.invoke({"query": question})
#         web_results = "\n".join([d["content"] for d in docs])
#         web_results = Document(page_content=web_results)
#         documents.append(web_results)
#
#         return {"documents": documents, "question": question}
#
#     ### Edges
#
#     def decide_to_generate(state):
#         """
#         Determines whether to generate an answer, or re-generate a question.
#
#         Args:
#             state (dict): The current graph state
#
#         Returns:
#             str: Binary decision for next node to call
#         """
#
#         print("---ASSESS GRADED DOCUMENTS---")
#         state["question"]
#         web_search = state["web_search"]
#         state["documents"]
#
#         if web_search == "Yes":
#             # All documents have been filtered check_relevance
#             # We will re-generate a new query
#             print(
#                 "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
#             )
#             return "transform_query"
#         else:
#             # We have relevant documents, so generate answer
#             print("---DECISION: GENERATE---")
#             return "generate"
#
#     async def process(self, state: State) -> State:
#         task = state.get("results").get(state.get("prev_agent"))[-1]
#         result = None
#         response = await self._chain.ainvoke({"task": [HumanMessage(content=task)]})
#         result = f"[Kết quả tính toán] {response.content}"
#         print("rag")
#         current_tasks = state.get("tasks", {})
#         current_results = state.get("results", {})
#
#         current_tasks.setdefault(self._agent_name, []).append(task)
#
#         current_results.setdefault(self._agent_name, []).append(result)
#         state.update(
#             human=False,
#             next_agent="writer",
#             prev_agent=self._agent_name,
#             tasks=current_tasks,
#             results=current_results,
#         )
#         return state
