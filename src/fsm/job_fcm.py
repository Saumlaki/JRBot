from aiogram.fsm.state import StatesGroup, State

class JobFCM(StatesGroup):
    """"FSM для gpt
    """
    prof = State() # профессия
    salary = State() # оклад
    end = State() # оклад