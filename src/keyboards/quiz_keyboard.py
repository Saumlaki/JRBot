from aiogram import types

from src.ather.prefix import Prefix

prefix = Prefix.QUIZ.value #%!% Поменяй в новом модуле

def get_start_keyboard():
    """Стартовая клавиатура игры в квиз. Позволяет выбрать варианты как ранее определенную тему так и тему на выбор"""
    buttons = [
        [types.InlineKeyboardButton(text="Животные"     , callback_data= f"{prefix}_theme_animals"),
         types.InlineKeyboardButton(text="Рыбы"         , callback_data= f"{prefix}_theme_fish"),
         types.InlineKeyboardButton(text="Растения"     , callback_data= f"{prefix}_theme_plants")],
        [types.InlineKeyboardButton(text="Космос"       , callback_data= f"{prefix}_theme_space"),
         types.InlineKeyboardButton(text="Наша планета" , callback_data= f"{prefix}_theme_earth"),
         types.InlineKeyboardButton(text="Любая тема"   , callback_data= f"{prefix}_theme_any")],
        [types.InlineKeyboardButton(text="Закончить"    , callback_data= f"{prefix}end")]
         ]
    return types.InlineKeyboardMarkup(inline_keyboard = buttons)

def get_main_keyboard(button_texts : []):
    """Клавиатура выбора варианта ответа"""
    buttons_answer = [types.InlineKeyboardButton(text=text, callback_data= f"{prefix}_answer_" + text) for text in button_texts]

    buttons = [buttons_answer,
               [types.InlineKeyboardButton(text="Выбрать другую тему"   , callback_data=f"{prefix}start"),
                types.InlineKeyboardButton(text="Закончить"             , callback_data= f"{prefix}end")]]
    return types.InlineKeyboardMarkup(inline_keyboard = buttons)

def get_empty_keyboard():
    """Клавиатура для отображения пустого поля"""
    return types.InlineKeyboardMarkup(inline_keyboard = [])