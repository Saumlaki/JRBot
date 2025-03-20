from aiogram.fsm.state import StatesGroup, State

class JobFCM(StatesGroup):
    """"FSM для gpt
    """
    start = State() # Начальное состояние
    name = State() # Имя
    prof = State() # профессия
    prof = State() # оклад