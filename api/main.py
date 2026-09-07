from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline.rag_qa import rag_answer
from rag_pipeline.query_database import retrieve_knowledge

MODEL_NAME = "BAAI/bge-small-zh-v1.5"

app = FastAPI()

# Route（路由）：规定什么 HTTP 请求应该交给哪个 Python 函数处理
@app.get("/health")
# HTTP Method：GET
# Path：/health
def health():
    return {"status": "ok"}

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(request: AskRequest):
    answer = rag_answer(
        request.question,
        MODEL_NAME,
        debug=False
    )

    return {
        "question": request.question,
        "answer": answer
    }


class SearchRequest(BaseModel):
    question: str
    top_k: int = 3

@app.post("/search")
def search(request: SearchRequest):
    results = retrieve_knowledge(
        request.question,
        request.top_k
    )

    return {
        "question": request.question,
        "results": results
    }
