import re
from collections import defaultdict

from bs4 import BeautifulSoup

from mood_prediction.schemas import EmotionalStatePredictionResult
from .emotion_service import EmotionService
from .mood_service import MoodService
from .translator_service import TranslatorService


class EmotionalStatePredictionService:
    emotion_service = EmotionService
    mood_service = MoodService

    @classmethod
    def predict(cls, text: str) -> EmotionalStatePredictionResult:
        normalized_text = cls._normalize_text(text)
        paragraphs = cls.split_text_into_paragraphs(normalized_text)

        if len(paragraphs) == 1:
            return cls._handle_single_paragraph(paragraphs[0])

        return cls._handle_multiple_paragraphs(paragraphs)

    @classmethod
    def _handle_single_paragraph(cls, paragraph: str) -> EmotionalStatePredictionResult:
        emotions_frequency = cls.emotion_service.determine_paragraph_emotions(paragraph)
        mood_name, _, distances = cls.mood_service.determine_paragraph_mood(emotions_frequency)
        mood_percentages = cls.mood_service.determine_distribution(distances)
        return EmotionalStatePredictionResult(
            dominant_mood_name=mood_name,
            distribution=mood_percentages,
            emotions_frequency=emotions_frequency
        )

    @classmethod
    def _handle_multiple_paragraphs(cls, paragraphs: list[str]) -> EmotionalStatePredictionResult:
        moods_pads = defaultdict(list)
        text_emotions_frequency = {}
        for paragraph in paragraphs:
            emotions_frequency = cls.emotion_service.determine_paragraph_emotions(paragraph)
            cls.add_dict(text_emotions_frequency, emotions_frequency)
            mood_name, mood_pad, _ = cls.mood_service.determine_paragraph_mood(emotions_frequency)
            moods_pads[mood_name].append(mood_pad)

        final_mood, mood_percentages = MoodService.determine_general_mood(moods_pads)
        return EmotionalStatePredictionResult(
            dominant_mood_name=final_mood,
            distribution=mood_percentages,
            emotions_frequency=text_emotions_frequency
        )

    @classmethod
    def _normalize_text(cls, text: str) -> str:
        return TranslatorService.translate(text)

    @staticmethod
    def split_text_into_paragraphs(text: str) -> list[str]:
        """
           Розділяє текст на абзаци, враховуючи:
           - plain text з переносами рядків
           - HTML (<p>, <br>)
           """

        # Якщо це HTML
        if "<" in text and ">" in text:
            soup = BeautifulSoup(text, "html.parser")

            # Замінюємо <br> на перенос рядка
            for br in soup.find_all("br"):
                br.replace_with("\n")

            # Отримуємо всі абзаци з <p>
            paragraphs = [p.get_text(separator="\n", strip=True) for p in soup.find_all("p")]

            # Якщо немає <p>, ділимо за подвійним переносом
            if not paragraphs:
                clean_text = soup.get_text("\n", strip=True)
                paragraphs = re.split(r'\n\s*\n', clean_text)
        else:
            # Якщо це звичайний текст
            # Нормалізуємо переноси рядків
            normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
            paragraphs = re.split(r'\n\s*\n', normalized_text.strip())

        # Прибираємо зайві пробіли з кожного абзацу
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs

    @staticmethod
    def add_dict(main_dict, new_dict):
        for key, value in new_dict.items():
            main_dict[key] = main_dict.get(key, 0) + value
