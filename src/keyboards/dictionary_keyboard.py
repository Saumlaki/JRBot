from aiogram import types
from src.ather.prefix import Prefix

prefix = Prefix.DICTIONARY.value  # %!% Поменяй в новом модуле


def get_start_keyboard():
    """Стартовая клавиатура для изучения слов. Позволяет выбрать варианты:
    - Выучить новое слово - берем новое слово из gpt
    - Повторить то выучил ранее - берем список слов из БД по имени пользователя и повторяем их от свежих к старым
    - Повторить трудные - берем слова на которых чаще всего делаем ошибки и повторяем их"""
    buttons = [
        [types.InlineKeyboardButton(text="Добавить слово", callback_data=f"{prefix}add"),
         types.InlineKeyboardButton(text="Показать слова", callback_data=f"{prefix}show"),
         types.InlineKeyboardButton(text="Начать изучение", callback_data=f"{prefix}learn")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_add_keyboard():
    """Клавиатура добавления слов
    - Пропустить - пропускает текущее слово, его не учим
    - Добавить к изучению - добавляет текущее слово в список изучения
    - Начать изучение - начинаем изучать ранее добавленные слова"""
    buttons = [
        [types.InlineKeyboardButton(text="Пропустить", callback_data=f"{prefix}next"),
         types.InlineKeyboardButton(text="Добавить к изучению", callback_data=f"{prefix}add"),
         types.InlineKeyboardButton(text="Начать изучение", callback_data=f"{prefix}learn")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

def get_end_keyboard():
    """Клавиатура окончания словарной тренировки"""
    buttons = [
        [ types.InlineKeyboardButton(text="Закончить"   , callback_data=f"{prefix}end")]]
    return  types.InlineKeyboardMarkup(inline_keyboard = buttons)

def get_empty_keyboard():
    """Клавиатура для отображения пустого поля"""
    return types.InlineKeyboardMarkup(inline_keyboard=[])



