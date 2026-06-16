#create prompt input using post operation

from fastapi import FastAPI
import fastapi
from ragapp.api.prompt_request import PromptRequest
from ragapp.utils.rag_engine import receive_prompt

app=FastAPI(
    title="RAG pipeline API",
    description="API for RAG pipeline",
    version="1.0.0"
    
)
@app.post("/prompt")
def create_prompt_input(prompt_request: PromptRequest):
    
     return receive_prompt(prompt_request.prompt)
    