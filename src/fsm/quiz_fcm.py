from aiogram.fsm.state import StatesGroup, State

class QuizFCM(StatesGroup):
    """"FSM для квиза
    """
    choosing_theme = State() # в данном состоянии не выбрана тема
    selected_theme = State() # в данном состоянии выбрана тема
    answer_question = State() # в данном состоянии происходит ответ на вопрос