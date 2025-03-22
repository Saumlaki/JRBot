from aiogram import Router, types
from aiogram.filters import Command

from src.ather.data_session_collector import DataSessionCollector
from src.ather.prefix import Prefix
from src.ather.message_templates import message_templates
from src.db import db_init

from src.keyboards.keyboard_collector import keyboard_collector
from src.forms.inline_form import InlineForm

prefix = Prefix.MAIN.value  # %!% Поменяй в новом модуле

router = Router()


@router.message(Command('start'))
async def cmd_start(msg: types.Message, data_session_collector: DataSessionCollector):
    """Стартовый диалог при запуске бота"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)
    data_session.clear()

    await InlineForm(msg=msg,
                     main_text=message_templates.get_start_message(prefix),
                     footer_text=message_templates.get_start_message_f(prefix),
                     keyboard=keyboard_collector.get_start_keyboard(prefix),
                     is_md_txt=False).answer()


@router.message(Command('dict'))
async def cmd_dict(msg: types.Message):
    """Вспомогательная команда инициализации словаря"""
    db_init.init_db()

    await InlineForm(msg=msg,
                     main_text="Словарь инициализирован",
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix),
                     is_md_txt=False).answer()

    await InlineForm(msg=msg,
                     main_text=message_templates.get_start_message(prefix),
                     footer_text=message_templates.get_start_message_f(prefix),
                     keyboard=keyboard_collector.get_start_keyboard(prefix),
                     is_md_txt=False).answer()
