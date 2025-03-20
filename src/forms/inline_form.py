from abc import ABC

from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from src.forms.abstract_form import AbstractForm


class InlineForm(AbstractForm):

    def __init__(self, msg: Message | CallbackQuery, main_text: str, footer_text: str | None, keyboard: InlineKeyboardMarkup):
        super().__init__(msg, main_text, footer_text, keyboard)

    def answer(self):
        self.main_text = self.main_text.replace("!", "\!")
        self.main_text = self.main_text.replace(".", "\.")
        self.main_text = self.main_text.replace("-", "\-")
        self.main_text = self.main_text.replace("(", "\(")
        self.main_text = self.main_text.replace(")", "\)")
        return self.msg.answer(text = "".join([self.main_text, f"\n\n{self.footer_text}" if len(self.footer_text) > 0 else ""]),
                               reply_markup = self.keyboard)

    def edit(self):
        return self.msg.edit_text(text = "".join([self.main_text, f"\n\n{self.footer_text}" if len(self.footer_text) > 0 else ""]),
                                  reply_markup = self.keyboard,)

