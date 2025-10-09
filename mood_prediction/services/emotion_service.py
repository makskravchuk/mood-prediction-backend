from collections import defaultdict

from mood_prediction.enums import EmotionName
from mood_prediction.machine_learning import EmotionClassifier
from nltk.tokenize import sent_tokenize


class EmotionService:
    classifier = EmotionClassifier

    @classmethod
    def determine_sentences_window_emotion(cls, sentences_window: str) -> EmotionName:
        result = cls.classifier.predict_main_emotion(sentences_window)
        return EmotionName(result)

    @classmethod
    def determine_paragraph_emotions(cls, paragraph: str, window_radius=2) -> dict[EmotionName, int]:
        sentences = cls.split_paragraph_into_sentences(paragraph)
        emotions_frequency = defaultdict(int)
        for i, current_sentence in enumerate(sentences):
            left = max(0, i - window_radius)
            right = min(len(sentences), i + window_radius + 1)
            emotion_name = cls.determine_sentences_window_emotion(" ".join(sentences[left:right]))
            emotions_frequency[emotion_name] += 1  # weight
        return emotions_frequency

    @staticmethod
    def split_paragraph_into_sentences(paragraph: str, language="english") -> list[str]:
        return sent_tokenize(paragraph, language=language)

    @classmethod
    def determine_distribution(cls, emotions_frequency: dict[EmotionName, int]) -> dict[EmotionName, float]:
        total = sum(emotions_frequency.values())
        emotion_percentages = {emotion: (frequency / total) * 100 for emotion, frequency in emotions_frequency.items()}
        return emotion_percentages
