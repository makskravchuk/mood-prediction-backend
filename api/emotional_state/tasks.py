from celery import shared_task

from api.emotional_state.schemas import PolarityDTO, MoodDTO, MoodDistributionDTO, EmotionDTO, EmotionFrequencyDTO, \
    ResultDTO
from mood_prediction import EmotionalStatePredictionService, MOOD_DICT, EMOTION_DICT
from mood_prediction.services import EmotionService


@shared_task(bind=True)
def predict_emo(self, text: str) -> dict:
    result = EmotionalStatePredictionService.predict(text)
    dominant_mood = MOOD_DICT[result.dominant_mood_name]
    polarity = dominant_mood.polarity
    distribution = []
    for mood_name, percentage in result.distribution.items():
        mood = MOOD_DICT[mood_name]
        mood_dto = MoodDTO.model_validate(mood)
        distribution_dto = MoodDistributionDTO(**mood_dto.model_dump(), percentage=percentage)
        distribution.append(distribution_dto)

    emotions_frequency = []
    emotions_frequency_percentage = EmotionService.determine_distribution(emotions_frequency=result.emotions_frequency)
    for emotion_name, percentage in emotions_frequency_percentage.items():
        emotion = EMOTION_DICT[emotion_name]
        emotion_dto = EmotionDTO.model_validate(emotion)
        emotion_frequency_dto = EmotionFrequencyDTO(**emotion_dto.model_dump(), percentage=percentage)
        emotions_frequency.append(emotion_frequency_dto)

    result_dto = ResultDTO(
        polarity=PolarityDTO.model_validate(polarity),
        dominant_mood=MoodDTO.model_validate(dominant_mood),
        mood_distribution=distribution,
        emotions_frequency=emotions_frequency
    )
    return result_dto.model_dump()
