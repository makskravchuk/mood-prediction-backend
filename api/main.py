import uvicorn
from fastapi import FastAPI
from .emotional_state import emotional_state_router

app = FastAPI(
    title="Emotional State Prediction API",
)

app.include_router(emotional_state_router, prefix="/api/emotional_state")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
