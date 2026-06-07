from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import build_chain

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="YouTube Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache built chains per video_id so we don't rebuild on every message
chain_cache: dict = {}


class LoadRequest(BaseModel):
    video_id: str


class ChatRequest(BaseModel):
    video_id: str
    question: str


@app.get("/")
def root():
    return {"status": "YouTube Chatbot API is running"}


@app.post("/load")
def load_video(req: LoadRequest):
    try:
        chain_cache[req.video_id] = build_chain(req.video_id)
        return {"status": "ready", "video_id": req.video_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load video: {str(e)}")


@app.post("/chat")
def chat(req: ChatRequest):
    if req.video_id not in chain_cache:
        raise HTTPException(status_code=400, detail="Video not loaded. Call /load first.")
    try:
        chain = chain_cache[req.video_id]
        answer = chain.invoke(req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")
