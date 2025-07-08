from langchain.chains import RetrievalQA
from langchain_together import Together
from src.config.setup import TOGETHER_API_KEY
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate

model = Together(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    temperature=0.1,
    top_p=0.9,
    repetition_penalty=1.3,
    max_tokens=512,
    together_api_key=TOGETHER_API_KEY,
)

def create_qa_chain(vector_db: FAISS, prompt: PromptTemplate) -> RetrievalQA:
    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return qa_chain
