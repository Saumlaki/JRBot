from aiogram.fsm.state import StatesGroup, State

class TalkFPGPTFCM(StatesGroup):
    """"FSM для gpt
    """
    step1 = State() #
    step2 = State() # состояние в котором ведется разговор