from typing import Optional, List

import numpy as np

from mood_prediction import dictionaries
from mood_prediction.dictionaries import EMOTIONS_TO_MOOD
from mood_prediction.enums import EmotionName, MoodName


class MoodService:

    @classmethod
    def _get_mood_from_emotion(cls, emotion: EmotionName) -> Optional[MoodName]:
        for mood, emotions in EMOTIONS_TO_MOOD.items():
            if emotion in emotions:
                return mood
        return None

    @classmethod
    def sort_into_moods(cls, emotions_frequency: dict[EmotionName, int]) -> dict[MoodName, dict[EmotionName, int]]:
        emotions_by_moods = {}
        for emotion, number in emotions_frequency.items():
            mood = cls._get_mood_from_emotion(emotion)
            if mood is not None:
                emotions_by_moods.setdefault(mood, {})[emotion] = number
        return emotions_by_moods

    @classmethod
    def determine_paragraph_mood(cls,
                                 emotions_frequency: dict[EmotionName, int]
                                 ) -> tuple[MoodName, np.ndarray, dict[MoodName, np.floating]]:
        emotions_by_moods = cls.sort_into_moods(emotions_frequency)
        moods_data = {}
        for mood, emotions in emotions_by_moods.items():
            mood_pad = np.array([0.0, 0.0, 0.0])
            number = 0
            for name, frequency in emotions.items():
                number += frequency
                mood_pad += dictionaries.EMOTION_DICT[name].pad * frequency

            moods_data[mood] = {'pad': mood_pad, 'number': number}

        distances = {mood: np.linalg.norm(data['pad']) for mood, data in moods_data.items()}
        final_mood_name = max(distances.items(), key=lambda x: x[1])[0]

        final_pad = moods_data[final_mood_name]['pad'] / moods_data[final_mood_name]['number']

        return final_mood_name, final_pad, distances

    @classmethod
    def determine_general_mood(cls,
                               moods_pads: dict[MoodName, List[np.ndarray]]) -> tuple[MoodName, dict[MoodName, float]]:
        if len(moods_pads) == 1:
            mood_name = list(moods_pads.keys())[0]
            return mood_name, {mood_name: 100.0}

        distances = {}
        for mood, pads in moods_pads.items():
            pad = sum(pads)
            distances[mood] = np.linalg.norm(pad)

        dominant_mood = max(distances.items(), key=lambda x: x[1])[0]
        mood_percentages = cls.determine_distribution(distances)

        return dominant_mood, mood_percentages

    @classmethod
    def determine_distribution(cls, distances: dict[MoodName, np.floating]) -> dict[MoodName, float]:
        total_distance = sum(distances.values())
        if total_distance == 0:
            if len(distances) == 1:
                only_key = next(iter(distances))
                if only_key == MoodName.NEUTRAL:
                    return {MoodName.NEUTRAL: 100.0}
            return {mood: 0.0 for mood in distances}
        else:
            mood_percentages = {mood: (distance / total_distance) * 100 for mood, distance in distances.items()}
        return mood_percentages
