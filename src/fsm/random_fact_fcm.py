from aiogram.fsm.state import StatesGroup, State

class RandomFactFCM(StatesGroup):
    """FSM для случайного факта\n
    - choosing_theme: Выбор темы\n
    - selected_theme: Тема выбрана"""
    choosing_theme = State() # в данном состоянии не выбрана тема
    selected_theme = State() # в данном состоянии выбрана тема