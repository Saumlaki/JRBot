from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.ather.prefix import Prefix

prefix = Prefix.TALK_FP.value #%!% Поменяй в новом модуле

def get_start_keyboard():
    """Стартовая клавиатура для общения с gpt.
    Вибераем личность
    """
    buttons = [
        [InlineKeyboardButton(text="Мастер Йода"        , callback_data= f"{prefix}_ioda"),
         InlineKeyboardButton(text="Бендер "            , callback_data= f"{prefix}_bender"),
         InlineKeyboardButton(text="Капитан Флинт"      , callback_data= f"{prefix}_flint")],
        [InlineKeyboardButton(text="Закончить"          , callback_data= f"{prefix}end")]
         ]
    return InlineKeyboardMarkup(inline_keyboard = buttons)

def get_main_keyboard():
    """Клавиатура окончания разговора"""
    buttons = [[InlineKeyboardButton(text="Закончить", callback_data=f"{prefix}end")]]
    return InlineKeyboardMarkup(inline_keyboard = buttons)

def get_empty_keyboard():
    """Клавиатура для отображения пустого поля"""
    return InlineKeyboardMarkup(inline_keyboard = [])

