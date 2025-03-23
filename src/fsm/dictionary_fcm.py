from aiogram.fsm.state import StatesGroup, State

class DictionaryFCM(StatesGroup):
    """"FSM для gpt
    """
    add = State() # добавление слова
    learn  =State() # Учим слова