import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import InputMediaPhoto
from dotenv import load_dotenv

from mood_prediction import EmotionalStatePredictionService
from . import answers
from .tools import form_prediction_response, build_mood_chart, build_emotion_chart

load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(answers.GREETING)
    await message.answer(answers.ASK_TEXT)


@dp.message(F.text)
async def handle_text(message: types.Message):
    await message.answer(answers.WAIT_TEXT)
    result = EmotionalStatePredictionService.predict(message.text)
    text_response = form_prediction_response(result)
    mood_chart = build_mood_chart(result.distribution)
    emotion_chart = build_emotion_chart(result.emotions_frequency)
    media = [
        InputMediaPhoto(media=mood_chart, caption=text_response),
        InputMediaPhoto(media=emotion_chart),
    ]
    await message.answer_media_group(media)
    await message.answer(answers.ASK_TEXT)


async def launch():
    await dp.start_polling(bot)
