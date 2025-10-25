from typing import Optional

from pydantic import BaseModel, ConfigDict, field_serializer


class TextRequest(BaseModel):
    text: str


class TaskResponse(BaseModel):
    task_id: str
    status: str


class BaseStateDTO(BaseModel):
    en_name: str
    uk_name: str
    color: str


class EmotionDTO(BaseStateDTO):
    emoji: str

    model_config = ConfigDict(
        from_attributes=True
    )


class PercentageDTO(BaseModel):
    percentage: float

    @field_serializer('percentage', when_used='json')
    def serialize_percentage(self, percentage: float) -> str:
        return f"{percentage:.2f}"


class EmotionFrequencyDTO(EmotionDTO, PercentageDTO):
    pass


class PolarityDTO(BaseStateDTO):
    sign: str
    model_config = ConfigDict(
        from_attributes=True
    )


class MoodDTO(BaseStateDTO):
    emoji: str
    model_config = ConfigDict(
        from_attributes=True
    )


class MoodDistributionDTO(MoodDTO, PercentageDTO):
    pass


class ResultDTO(BaseModel):
    polarity: PolarityDTO
    dominant_mood: MoodDTO
    mood_distribution: list[MoodDistributionDTO]
    emotions_frequency: list[EmotionFrequencyDTO]


class ResultResponse(TaskResponse):
    result: Optional[ResultDTO]
