from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.ather.prefix import Prefix


def get_start_keyboard():
    """Клавиатура начального экрана бота"""
    buttons = [
        [InlineKeyboardButton(text="Случайный факт"                   , callback_data= f"{Prefix.RANDOM_FACT.value}start"),
         InlineKeyboardButton(text="Игра в КВИЗ"                      , callback_data= f"{Prefix.QUIZ.value}start")],
        [InlineKeyboardButton(text="Пообщаться с GPT"                 , callback_data= f"{Prefix.TALK_GPT.value}start"),
         InlineKeyboardButton(text="Поговорить с известной личностью" , callback_data= f"{Prefix.TALK_FP.value}start")],
        [InlineKeyboardButton(text="Помощь с резюме"                  , callback_data= f"{Prefix.JOB.value}start"),
         InlineKeyboardButton(text="Словарный тренажер"               , callback_data= f"{Prefix.DICTIONARY.value}start")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)