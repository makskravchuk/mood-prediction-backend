import os

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class EmotionClassifier:
    __BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    __MODEL_PATH = os.path.join(__BASE_DIR, "goemotions_model")
    __MODEL_NAME = "monologg/bert-base-cased-goemotions-original"
    tokenizer = AutoTokenizer.from_pretrained(__MODEL_PATH, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(__MODEL_PATH, local_files_only=True)

    @classmethod
    def predict_main_emotion(cls, text: str) -> str:
        inputs = cls.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = cls.model(**inputs)
        logits = outputs.logits
        probabilities = torch.sigmoid(logits)[0]
        max_index = torch.argmax(probabilities).item()
        return cls.model.config.id2label[max_index]

    @classmethod
    def download_model(cls):
        if not os.path.exists(cls.__MODEL_PATH):
            tokenizer = AutoTokenizer.from_pretrained(cls.__MODEL_NAME)
            model = AutoModelForSequenceClassification.from_pretrained(cls.__MODEL_NAME)
            tokenizer.save_pretrained(cls.__MODEL_PATH)
            model.save_pretrained(cls.__MODEL_PATH)
