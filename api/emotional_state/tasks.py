from celery import shared_task
from celery.result import AsyncResult

from mood_prediction import EmotionalStatePredictionService, EmotionalStatePredictionResult


@shared_task(bind=True)
def predict_emo(self, text: str) -> dict:
    result = EmotionalStatePredictionService.predict(text)
    dominant_mood = result.dominant_mood_name.value
    distribution = {k.value: v for k, v in result.distribution.items()}
    emotions_frequency = {k.value: v for k, v in result.emotions_frequency.items()}
    return {
        "dominant_mood": dominant_mood,
        "distribution": distribution,
        "emotions_frequency": emotions_frequency
    }
