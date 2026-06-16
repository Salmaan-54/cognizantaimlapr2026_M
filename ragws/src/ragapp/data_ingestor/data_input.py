#read the food delivery policy from data folder create embeddings
import os
from dotenv import load_dotenv
from langchain_classic.document_loaders import Docx2txtLoader, TextLoader,PyPDFLoader

env_path = os.path.join(os.path.dirname(__file__),'..', '.env')
load_dotenv(env_path)

def load_documents(dir_path):
    documents=[]

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if filename.endswith('.txt'):            
            loader=TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
        elif filename.endswith('.pdf'):            
            loader=PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith('.docx'):
            loader=Docx2txtLoader(file_path)
            documents.extend(loader.load())
    return documents