#rag engine will load data from vector database
#send prompt to llm
#llm will query the vector database and return relevant information

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA
env_path= os.path.join(os.path.dirname(__file__), '..','.env')
load_dotenv(env_path)

def load_data_from_vector_db():
    persistent_directory = os.getenv("persist_directory")
    if not persistent_directory:
        raise ValueError("persist_directory is not set in the environment variables.")
    #read embeddings from persistent directory
    embeddings= HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    #read from vector database
    vector_db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)
    retriever = vector_db.as_retriever(
        search_kwargs={"k": 3}
    )
    return retriever

def load_llm(retriever):
    #define open ai llm
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        #chain_type_kwargs={"prompt": prompt_template}
    )

    return rag_chain

def prompt_query(question:str):
    #read the prompt
    retriever = load_data_from_vector_db()
    ragchain= load_llm(retriever)
    answer= ragchain.invoke({
        "query": question
    })
    return {
        "answer": answer,
        "sources": [
            doc.metadata for doc in answer["source_documents"]
        ]
    }