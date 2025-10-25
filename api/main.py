import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .emotional_state import emotional_state_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Emotional State Prediction API",
)

origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(emotional_state_router, prefix="/api/emotional_state")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
