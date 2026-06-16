#rag engine will load data from vector database
#send prompt to llm
#llm will query the vector database and return relevant information

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
env_path= os.path.join(os.path.dirname(__file__), '..','.env')
load_dotenv(env_path)

def load_data_from_vector_db():
    persistent_directory = os.getenv("persist_directory")
    #read embeddings from persistent directory
    embeddings= HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
