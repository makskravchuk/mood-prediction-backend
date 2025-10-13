from typing import Optional

from pydantic import BaseModel


class TextRequest(BaseModel):
    text: str


class TaskResponse(BaseModel):
    task_id: str
    status: str


class ResultDTO(BaseModel):
    dominant_mood: str
    distribution: dict[str, float]
    emotions_frequency: dict[str, int]


class ResultResponse(TaskResponse):
    result: Optional[ResultDTO]
