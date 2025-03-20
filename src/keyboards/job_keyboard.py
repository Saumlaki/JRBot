from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.ather.prefix import Prefix

prefix = Prefix.JOB.value #%!% Поменяй в новом модуле

def get_start_keyboard():
    """Стартовая клавиатура помошника составления резюме"""
    buttons = [
        [InlineKeyboardButton(text="Начать"    , callback_data= f"{prefix}go")],
        [InlineKeyboardButton(text="Закончить" , callback_data= f"{prefix}end")]
         ]
    return InlineKeyboardMarkup(inline_keyboard = buttons)

def get_main_keyboard():
    """Клавиатура ввода информации о резюме"""
    buttons = [
        [   InlineKeyboardButton(text="Назад"    , callback_data=f"{prefix}back"),
            InlineKeyboardButton(text="Заново"   , callback_data=f"{prefix}start"),
            InlineKeyboardButton(text="Закончить", callback_data=f"{prefix}end")]]
    return InlineKeyboardMarkup(inline_keyboard = buttons)

def get_end_keyboard():
    """Клавиатура окончания разговора"""
    buttons = [
        [   InlineKeyboardButton(text="Заново"   , callback_data=f"{prefix}back"),
            InlineKeyboardButton(text="Закончить", callback_data=f"{prefix}end")]]
    return InlineKeyboardMarkup(inline_keyboard = buttons)

def get_empty_keyboard():
    """Клавиатура для отображения пустого поля"""
    return InlineKeyboardMarkup(inline_keyboard = [])