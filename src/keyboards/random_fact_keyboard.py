from aiogram import types
from src.ather.prefix import Prefix


prefix = Prefix.RANDOM_FACT.value #%!% Поменяй в новом модуле


def get_start_keyboard():
    """Стартовая клавиатура интересных фактов. Позволяет выбрать варианты:
    - Удиви меня - представляет факт по случайной теме
    - Хватит - переходит на стартовое окно бота"""
    buttons = [
        [types.InlineKeyboardButton(text="Удиви меня"   , callback_data= f"{prefix}next"),
         types.InlineKeyboardButton(text="Хватит"       , callback_data= f"{prefix}end")]
         ]
    return types.InlineKeyboardMarkup(inline_keyboard = buttons)

def get_main_keyboard():
    """Клавиатура перехода к новому факту. Позволяет выбрать варианты:
    - Еще - пропускает текущее слово, его не учим
    - Хватит - переходит на стартовое окно бота
    - Выбрать другую тему - переходит к окну выбора тем"""
    buttons = [
        [types.InlineKeyboardButton(text="Еще"                  , callback_data= f"{prefix}next"),
         types.InlineKeyboardButton(text="Хватит"               , callback_data= f"{prefix}end"),
         types.InlineKeyboardButton(text="Выбрать другую тему"  , callback_data= f"{prefix}start")]
         ]
    return types.InlineKeyboardMarkup(inline_keyboard = buttons)

def get_empty_keyboard():
    """Клавиатура для отображения пустого поля"""
    return types.InlineKeyboardMarkup(inline_keyboard = [])