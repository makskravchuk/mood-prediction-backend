import os

import deepl
from langdetect import detect
from dotenv import load_dotenv

load_dotenv()


class TranslatorService:
    deepl_client = deepl.DeepLClient(os.getenv("DEEPL_AUTH_KEY"))

    @classmethod
    def translate(cls, text: str, target_language: str = "EN-US") -> str:
        detected_language = detect(text)
        if detected_language.lower() != target_language[:2].lower():
            result = cls.deepl_client.translate_text(text, source_lang=detected_language, target_lang=target_language)
            return result.text
        else:
            return text
