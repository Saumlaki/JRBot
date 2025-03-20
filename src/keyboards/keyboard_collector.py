from aiogram.types import InlineKeyboardMarkup

from src.ather.prefix import Prefix
import src.keyboards.dictionary_keyboard  as dictionary_keyboards
import src.keyboards.random_fact_keyboard  as random_fact_keyboard
import src.keyboards.quiz_keyboard  as quiz_keyboard
import src.keyboards.main_keyboard  as main_keyboard
import src.keyboards.talk_gpt_keyboard  as talk_gpt_keyboard
import src.keyboards.talk_fp_gpt_keyboard  as talk_fp_gpt_keyboard
import src.keyboards.job_keyboard  as job_keyboard
import src.keyboards.dictionary_keyboard  as dictionary_keyboard

class KeyboardCollector:
    """"Содержит наборы клавиатур разделенных префиксами"""
    def __init__(self):
        self.start_keyboards = {} # Клавиатуры начала диалогов
        self.add_keyboards   = {} # Клавиатуры добавления
        self.main_keyboards  = {} # Основные клавиатуры
        self.empty_keyboard  = {} # Пустые клавиатуры

    def get_start_keyboard(self,  prefix : str)->InlineKeyboardMarkup:
        return self.start_keyboards.get(prefix)

    def add_start_keyboard(self, prefix : str, keyboard : InlineKeyboardMarkup):
        self.start_keyboards[prefix]= keyboard

    def get_empty_keyboard(self,  prefix : str)->InlineKeyboardMarkup:
        return self.empty_keyboard.get(prefix)

    def add_empty_keyboard(self, prefix : str, keyboard : InlineKeyboardMarkup):
        self.empty_keyboard[prefix]= keyboard

    def get_add_keyboard(self,  prefix : str)->InlineKeyboardMarkup:
        return self.add_keyboards.get(prefix)

    def add_add_keyboard(self, prefix : str, keyboard : InlineKeyboardMarkup):
        self.add_keyboards[prefix]= keyboard

    def get_main_keyboard(self,  prefix : str)->InlineKeyboardMarkup:
        return self.main_keyboards.get(prefix)

    def add_main_keyboard(self, prefix : str, keyboard : InlineKeyboardMarkup):
        self.main_keyboards[prefix]= keyboard
keyboard_collector = KeyboardCollector()

# Добавляем клавиатуры стартовых экранов
keyboard_collector.add_start_keyboard(Prefix.MAIN.value         , main_keyboard.get_start_keyboard())
keyboard_collector.add_start_keyboard(Prefix.RANDOM_FACT.value  , random_fact_keyboard.get_start_keyboard())
keyboard_collector.add_start_keyboard(Prefix.QUIZ.value         , quiz_keyboard.get_start_keyboard())
keyboard_collector.add_start_keyboard(Prefix.DICTIONARY.value   , dictionary_keyboards.get_start_keyboard())
keyboard_collector.add_start_keyboard(Prefix.TALK_GPT.value     , talk_gpt_keyboard.get_start_keyboard())
keyboard_collector.add_start_keyboard(Prefix.TALK_FP.value      , talk_fp_gpt_keyboard.get_start_keyboard())
keyboard_collector.add_start_keyboard(Prefix.JOB.value          , job_keyboard.get_start_keyboard())
keyboard_collector.add_start_keyboard(Prefix.DICTIONARY.value   , dictionary_keyboards.get_start_keyboard())

# Добавляем пустые клавиатуры
keyboard_collector.add_empty_keyboard(Prefix.RANDOM_FACT.value  , random_fact_keyboard.get_empty_keyboard())
keyboard_collector.add_empty_keyboard(Prefix.QUIZ.value         , quiz_keyboard.get_empty_keyboard())
keyboard_collector.add_empty_keyboard(Prefix.DICTIONARY.value   , dictionary_keyboards.get_empty_keyboard())
keyboard_collector.add_empty_keyboard(Prefix.TALK_GPT.value     , talk_gpt_keyboard.get_empty_keyboard())
keyboard_collector.add_empty_keyboard(Prefix.TALK_GPT.value     , talk_fp_gpt_keyboard.get_empty_keyboard())
keyboard_collector.add_empty_keyboard(Prefix.JOB.value          , job_keyboard.get_empty_keyboard())
keyboard_collector.add_empty_keyboard(Prefix.DICTIONARY.value   , dictionary_keyboards.get_empty_keyboard())

# Добавляем основные клавиатуры
keyboard_collector.add_main_keyboard(Prefix.RANDOM_FACT.value   , random_fact_keyboard.get_main_keyboard())
keyboard_collector.add_main_keyboard(Prefix.TALK_GPT.value      , talk_gpt_keyboard.get_main_keyboard())
keyboard_collector.add_main_keyboard(Prefix.TALK_FP.value       , talk_fp_gpt_keyboard.get_main_keyboard())
keyboard_collector.add_main_keyboard(Prefix.JOB.value           , job_keyboard.get_main_keyboard())
# keyboard_collector.add_main_keyboard(Prefix.DICTIONARY.value    , dictionary_keyboards.get_main_keyboard())

# Добавляем клавиатуры выбора/добавления
keyboard_collector.add_add_keyboard(Prefix.DICTIONARY.value , dictionary_keyboards.get_add_keyboard())