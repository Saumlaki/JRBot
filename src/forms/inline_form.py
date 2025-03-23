from abc import ABC

from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from src.forms.abstract_form import AbstractForm


class InlineForm(AbstractForm):

    def __init__(self, msg: Message | CallbackQuery, main_text: str, footer_text: str | None, keyboard: InlineKeyboardMarkup, is_md_txt = True):
        super().__init__(msg, main_text, footer_text, keyboard)

        if not is_md_txt:
            self.main_text = self.replace(self.main_text)


    def answer(self,separator="\n\n"):
        return self.msg.answer(text = "".join([self.main_text, f"{separator}{self.footer_text}" if len(self.footer_text) > 0 else ""]),
                               reply_markup = self.keyboard)

    def edit(self, separator="\n\n" ):
        return self.msg.edit_text(text = "".join([self.main_text, f"{separator}{self.footer_text}" if len(self.footer_text) > 0 else ""]),
                                  reply_markup = self.keyboard,)

    def replace(self, text):
        text = text.replace("!", "\!")
        text = text.replace(".", "\.")
        text = text.replace("-", "\-")
        text = text.replace("(", "\(")
        text = text.replace(")", "\)")
        text = text.replace("#", "\#")
        text = text.replace("+", "\+")
        text = text.replace("[", "\+")
        text = text.replace("]", "\+")

        return text

