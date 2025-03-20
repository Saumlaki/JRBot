from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.ather.prefix import Prefix

prefix = Prefix.TALK_GPT.value #%!% Поменяй в новом модуле

def get_start_keyboard():
    """Стартовая клавиатура для общения с gpt"""
    buttons = [
        [InlineKeyboardButton(text="Погода"       , callback_data= f"{prefix}_theme_weather"),
         InlineKeyboardButton(text="Работа "      , callback_data= f"{prefix}_theme_job"),
         InlineKeyboardButton(text="Любая тема"   , callback_data= f"{prefix}_theme_random")],
        [InlineKeyboardButton(text="Закончить"    , callback_data= f"{prefix}end")]
         ]
    return InlineKeyboardMarkup(inline_keyboard = buttons)

def get_main_keyboard():
    """Клавиатура окончания разговора"""
    buttons = [[InlineKeyboardButton(text="Закончить", callback_data=f"{prefix}end")]]
    return InlineKeyboardMarkup(inline_keyboard = buttons)

def get_empty_keyboard():
    """Клавиатура для отображения пустого поля"""
    return InlineKeyboardMarkup(inline_keyboard = [])