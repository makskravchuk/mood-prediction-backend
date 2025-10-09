from io import BytesIO

from aiogram.types import BufferedInputFile

from mood_prediction import EmotionalStatePredictionResult, EMOTION_DICT
from mood_prediction import MOOD_DICT
from mood_prediction.enums import MoodName, EmotionName
from mood_prediction.services import EmotionService
from telegram_bot.chart_builder import ChartBuilder
from telegram_bot.schemas import ChartDataCell


def form_prediction_response(result: EmotionalStatePredictionResult) -> str:
    mood = MOOD_DICT[result.dominant_mood_name]
    polarity = mood.polarity
    mood_distribution_filtered = {k: v for k, v in result.distribution.items() if v != 0}
    mood_distribution_str = ""
    for mood_name, percentage in mood_distribution_filtered.items():
        md = MOOD_DICT[mood_name]
        percentage_str = f"{int(percentage)}%" if percentage.is_integer() else f"{percentage:.2f}%"
        # row = f"\n🔹 {md.uk_name} {md.emoji} - {percentage_str}"
        row = f"\n🔹 {md.en_name.title()} {md.emoji} - {percentage_str}"
        mood_distribution_str += row

    emotions_frequency_percentage = EmotionService.determine_distribution(emotions_frequency=result.emotions_frequency)
    emotions_frequency_str = ""
    for emotion_name, percentage in emotions_frequency_percentage.items():
        emo = EMOTION_DICT[emotion_name]
        percentage_str = f"{int(percentage)}%" if percentage.is_integer() else f"{percentage:.2f}%"
        # row = f"\n🔸 {emo.uk_name} {emo.emoji} - {percentage_str}"
        row = f"\n🔸 {emo.en_name.title()} {emo.emoji} - {percentage_str}"
        emotions_frequency_str += row

    # return (f"🔎              Результати аналізу              🔎\n"
    #         f"\n– Текст є <b>{polarity.uk_name.lower()}</b> за емоційною полярністю.\n"
    #         f"\n– Домінуючий настрій: <b>{mood.uk_name.lower()}</b> {mood.emoji}\n"
    #         f"\n– Відсотковий роздподіл настроїв:\n {mood_distribution_str}\n"
    #         f"\n– Відносний частотний роздподіл емоцій:\n {emotions_frequency_str}"
    # )
    return (f"🔎              The analysis results              🔎\n"
            f"\n– The text is <b>{polarity.en_name.lower()}</b> in terms of emotional polarity.\n"
            f"\n– The dominant mood: <b>{mood.en_name.lower()}</b> {mood.emoji}\n"
            f"\n– Percentage distribution of moods:\n {mood_distribution_str}\n"
            f"\n– Relative frequency distribution of emotions:\n {emotions_frequency_str}"
    )


def build_mood_chart(mood_distribution: dict[MoodName, float]) -> BufferedInputFile:
    mood_distribution_filtered = {k: v for k, v in mood_distribution.items() if v != 0}
    data = []
    for mood_name, percentage in mood_distribution_filtered.items():
        md = MOOD_DICT[mood_name]
        # label = f"{md.uk_name} {md.emoji}"
        label = f"{md.en_name.title()} {md.emoji}"
        cell = ChartDataCell(label=label, color=md.color, value=percentage)
        data.append(cell)

    # chart = ChartBuilder.create_pie_chart(data, "Відсотковий розподіл настроїв")
    chart = ChartBuilder.create_pie_chart(data, "Percentage distribution of moods")
    return BufferedInputFile(chart.read(), filename="mood_chart.png")


def build_emotion_chart(emotions_frequency: dict[EmotionName, int]) -> BufferedInputFile:
    data = []
    emotions_frequency_percentage = EmotionService.determine_distribution(emotions_frequency=emotions_frequency)
    for emotion_name, value in emotions_frequency_percentage.items():
        emo = EMOTION_DICT[emotion_name]
        # label = f"{emo.uk_name} {emo.emoji}"
        label = f"{emo.en_name.title()} {emo.emoji}"
        cell = ChartDataCell(label=label, color=emo.color, value=value)
        data.append(cell)

    # chart = ChartBuilder.create_bar_chart(data, "Відносний частотний розподіл емоцій")
    chart = ChartBuilder.create_bar_chart(data, "Relative frequency distribution of emotions")
    return BufferedInputFile(chart.read(), filename="emotion_chart.png")
