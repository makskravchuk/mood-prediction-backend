from pydantic import BaseModel

from .enums import MoodName, EmotionName


class EmotionalStatePredictionResult(BaseModel):
    dominant_mood_name: MoodName
    distribution: dict[MoodName, float]
    emotions_frequency: dict[EmotionName, int]
