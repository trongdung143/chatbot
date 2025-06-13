import os
from langchain_core.tools import tool
from src.utils.vector_store import *
from langchain.prompts import PromptTemplate
from src.agents.agent3 import create_qa_chain


@tool
def rag_file(file_name: str, query: str) -> str:
    """
    Answer questions using information from a PDF or Word file with the Retrieval-Augmented Generation (RAG).

    Args:
        file_name (str): The name of the PDF file located in 'src/data/'.
        query (str): The user's question to be answered using the file content.

    Returns:
        str: The answer to the question or an error message.
    """
    try:
        pdf_data_path = f"src/data/{file_name}"
        file_base = os.path.splitext(file_name)[0]
        vector_db_path = f"src/agents/data/vectorstores/{file_base}"

        if not os.path.exists(vector_db_path):
            create_vector_db_from_file(pdf_data_path, vector_db_path)

        prompt = PromptTemplate(
            template="""
                You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
                Question: {question}
                Context: {context}
                Answer:
            """,
            input_variables=["context", "question"],
        )

        vector_db = read_vertors_db(vector_db_path)
        llm_chain = create_qa_chain(vector_db, prompt)
        result = llm_chain.invoke({"query": query})
        return f"{result['result']}"
    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}"


@tool
def rag_web(url: str, query: str) -> str:
    """
    Answer questions using information from a url with the Retrieval-Augmented Generation (RAG).

    Args:
        url (str): Website address to get data.
        query (str): The user's question to be answered using the web content.

    Returns:
        str: The answer to the question or an error message.
    """
    try:
        prompt = PromptTemplate(
            template="""
                You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
                Question: {question}
                Context: {context}            
                Answer:
            """,
            input_variables=["context", "question"],
        )
        vector_db = create_vector_db_from_text(url)
        llm_chain = create_qa_chain(vector_db, prompt)
        result = llm_chain.invoke({"query": query})
        return f"{result['result']}"
    except Exception as e:
        return f"An error occurred while processing: {str(e)}"


# @tool
# def search_web(query: str) -> str:
#     """
#     Answer questions using information from a url with the Retrieval-Augmented Generation (RAG).

#     Args:
#         url (str): Website address to get data.
#         query (str): The user's question to be answered using the file content.

#     Returns:
#         str: The answer to the question or an error message.
#     """
#     try:
#         prompt = PromptTemplate(
#             template="""
#                 You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
#                 Question: {question}
#                 Context: {context}
#                 Answer:
#             """,
#             input_variables=["context", "question"],
#         )

#         llm_chain = create_qa_chain(vector_db, prompt)
#         result = llm_chain.invoke({"query": query})
#         return f"{result['result']}"
#     except Exception as e:
#         return f"An error occurred while processing: {str(e)}"
