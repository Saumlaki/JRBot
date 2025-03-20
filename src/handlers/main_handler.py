from aiogram import Router, types
from aiogram.filters import Command

from src.ather.prefix import Prefix
from src.ather.message_templates import message_templates

from src.keyboards.keyboard_collector import keyboard_collector
from src.forms.inline_form import InlineForm


prefix = Prefix.MAIN.value #%!% Поменяй в новом модуле

router = Router()


@router.message(Command('start'))
async def cmd_start(msg: types.Message):
    """Стартовый диалог при запуске бота"""
    await InlineForm(msg= msg,
                    main_text= message_templates.get_start_message(prefix),
                    footer_text= message_templates.get_start_message_f(prefix),
                    keyboard= keyboard_collector.get_start_keyboard(prefix)).answer()