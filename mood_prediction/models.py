from typing import List

import numpy as np

from .enums import EmotionName


class Emotion:

    def __init__(self, en_name: str, uk_name: str, emoji: str, color: str, pleasure: float, arousal: float,
                 dominance: float) -> None:
        if not (-1 <= pleasure <= 1 and -1 <= arousal <= 1 and -1 <= dominance <= 1):
            raise ValueError("Values for pleasure, arousal, and dominance must be between -1 and 1.")

        self.en_name = en_name
        self.uk_name = uk_name
        self.emoji = emoji
        self.color = color
        self.__pleasure = pleasure
        self.__arousal = arousal
        self.__dominance = dominance
        self.__pad = np.array([pleasure, arousal, dominance])

    @property
    def pad(self) -> np.ndarray:
        return self.__pad

    def __str__(self):
        return f"{self.en_name} {self.emoji}"

    def __repr__(self):
        return f"{self.uk_name}({self.en_name.lower()}) {self.emoji}"


class EmotionalPolarity:

    def __init__(self, en_name: str, uk_name: str, sign: str):
        self.en_name = en_name
        self.uk_name = uk_name
        self.sign = sign

    def __str__(self):
        return f"{self.uk_name}"

    def __repr__(self):
        return f"{self.en_name} {self.sign}"


class Mood:

    def __init__(self, en_name: str, uk_name: str, emoji: str, color: str,
                 emotions: List[EmotionName], polarity: EmotionalPolarity):
        self.en_name = en_name
        self.uk_name = uk_name
        self.emoji = emoji
        self.emotions = emotions
        self.polarity = polarity
        self.color = color

    def check_affiliation(self, emotion: EmotionName) -> bool:
        return emotion in self.emotions

    def __str__(self):
        return f"{self.en_name} {self.emoji}"

    def __repr__(self):
        return f"{self.uk_name}({self.en_name.lower()}) {self.emoji}"
