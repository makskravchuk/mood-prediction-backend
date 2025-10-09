import asyncio

import nltk

from telegram_bot import launch
from mood_prediction.machine_learning import EmotionClassifier


def ensure_nltk_punkt():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')


if __name__ == "__main__":
    print("🔍 Checking NLTK resources...")
    ensure_nltk_punkt()

    print("🧠 Ensuring emotion model is ready...")
    EmotionClassifier.download_model()

    print("🤖 Launching Telegram bot...")
    asyncio.run(launch())
