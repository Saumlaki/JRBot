import abc
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup


class AbstractForm(abc.ABC):
    """Класс описывает интерфейс формы отправки сообщения
    """
    def __init__(self, msg : Message|CallbackQuery, main_text : str, footer_text: str, keyboard : InlineKeyboardMarkup|None):
        self.msg = msg
        self.main_text = main_text if main_text is not None else ""
        self.footer_text = footer_text if footer_text is not None else ""
        self.keyboard = keyboard

    @abc.abstractmethod
    def answer(self):
        pass

    @abc.abstractmethod
    def edit(self):
        pass
