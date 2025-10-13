import asyncio

import nltk

from telegram_bot import launch
from mood_prediction.machine_learning import EmotionClassifier



def ensure_nltk_resources():
    for resource in ("punkt", "punkt_tab"):
        try:
            nltk.data.find(f"tokenizers/{resource}")
        except LookupError:
            print(f"⬇️ Downloading NLTK resource: {resource}")
            nltk.download(resource)


if __name__ == "__main__":
    print("🔍 Checking NLTK resources...")
    ensure_nltk_resources()

    print("🧠 Ensuring emotion model is ready...")
    EmotionClassifier.download_model()
