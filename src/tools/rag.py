from langchain_core.tools import tool
from src.utils.vectorst import *
from langchain.prompts import PromptTemplate
from src.agents.analysis.agent3 import create_qa_chain


@tool
async def rag_file(file_name: str, question: str) -> str:
    """
    Answer questions using information from a PDF or Word file with the Retrieval-Augmented Generation (RAG).

    Args:
        file_name (str): The name.txt of the PDF file located in 'src/data/'.
        question (str): The user's question to be answered using the file content.

    Returns:
        str: The answer to the question or an error message.
    """
    try:
        pdf_data_path = f"src/data/{file_name}"
        file_base = os.path.splitext(file_name)[0]

        vector_db = await create_vector_db_from_file(pdf_data_path, file_base)

        prompt = PromptTemplate(
            template="""
                <s>[INST]
                You are an assistant for question-answering tasks. Use the following retrieved context to answer the question.
                If you don't know the answer, say you don't know. Answer in three sentences max.
                Context:
                {context}

                Question:
                {question}
                [/INST]
                """,
            input_variables=["context", "question"],
        )
        if vector_db is None:
            vector_db = await read_vectorstores(file_base)
        llm_chain = create_qa_chain(vector_db, prompt)
        result = await llm_chain.ainvoke({"query": question})
        return result["result"]
    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}"


@tool
async def rag_web(url: str, query: str) -> str:
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
                      <s>[INST]
                      You are an assistant for question-answering tasks. Use the following retrieved context to answer the question.
                      If you don't know the answer, say you don't know. Answer in three sentences max.
                      Context:
                      {context}

                      Question:
                      {question}
                      [/INST]
                      """,
            input_variables=["context", "question"],
        )
        vector_db = await create_vector_db_from_text(url)
        llm_chain = create_qa_chain(vector_db, prompt)
        result = await llm_chain.ainvoke({"query": query})
        return f"{result['result']}"
    except Exception as e:
        return f"An error occurred while processing: {str(e)}"
