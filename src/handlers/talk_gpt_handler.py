import json

from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from src.ather.message_templates import message_templates
from src.ather.prefix import Prefix

from src.ather.data_session_collector import DataSessionCollector
from src.forms.inline_form import InlineForm

from src.fsm.talk_gpt_fcm import TalkGPTFCM
from src.gpt.talk_gpt import TalkGPT
from src.keyboards.keyboard_collector import keyboard_collector

prefix = Prefix.TALK_GPT.value #%!% Поменяй в новом модуле

router = Router()
router.callback_query.filter(lambda clb : clb.data.startswith(prefix))

####################################################################################################
# Обработчики callback_query
####################################################################################################

@router.callback_query(F.data.endswith("start"))
async def cmd_start(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector):
    """Стартовый диалог разговора с gpt"""

    data_session = data_session_collector.get_data_session(cbq.from_user.id)
    data_session.gpt =TalkGPT()

    await state.set_state(TalkGPTFCM.step1)
    await InlineForm(msg= cbq.message,
                        main_text= cbq.message.md_text,
                        footer_text= "",
                        keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    data_session.msg_talk_gpt = await InlineForm(msg= cbq.message,
                    main_text= message_templates.get_start_message(prefix),
                    footer_text= message_templates.get_start_message_f(prefix),
                    keyboard= keyboard_collector.get_start_keyboard(prefix)).answer()

@router.callback_query(F.data.endswith(("_theme_weather", "_theme_job", "_theme_random")))
async def cmd_theme(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector):
    """Выбор темы в разговоре с gpt"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)

    answer_str = ""
    if cbq.data.endswith("_theme_weather"):
        answer_str = data_session.gpt.get_answer("Давай поговорим на тему: погода")
    elif cbq.data.endswith("_theme_job"):
        answer_str = data_session.gpt.get_answer("Давай поговорим на тему: работа")
    elif cbq.data.endswith("_theme_random"):
        answer_str = data_session.gpt.get_answer("Давай просто поболтаем")

    await state.set_state(TalkGPTFCM.step2)
    await InlineForm(msg= cbq.message,
                        main_text= cbq.message.md_text,
                        footer_text= "",
                        keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    data_session.msg_talk_gpt = await InlineForm(msg= cbq.message,
                        main_text= answer_str,
                        footer_text= "",
                        keyboard= keyboard_collector.get_main_keyboard(prefix)).answer()

@router.callback_query(F.data.endswith("end"))
async def cmd_end(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector):
    """Прекращаем разговор с gpt"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)
    answer_str = data_session.gpt.get_answer("Давай закончим разговор")
    data_session.msg_talk_gpt = None

    await state.clear()
    await InlineForm(msg=cbq.message,
                     main_text= cbq.message.md_text,
                     footer_text= "",
                     keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    await InlineForm(msg=cbq.message,
                         main_text=answer_str,
                         footer_text="",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix)).answer()

    await InlineForm(msg= cbq.message,
                    main_text= message_templates.get_start_message(Prefix.MAIN.value),
                    footer_text= message_templates.get_start_message_f(Prefix.MAIN.value),
                    keyboard= keyboard_collector.get_start_keyboard(Prefix.MAIN.value)).answer()

####################################################################################################
# Обработчики message
####################################################################################################

@router.message(F.text, TalkGPTFCM.step1)
async def cmd_msg_theme(msg : types.message, state: FSMContext, data_session_collector : DataSessionCollector):
    """Обработчик отвечает за ввод произвольной темы беседы"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)

    answer_str = data_session.gpt.get_answer(f"Давай поговорим на тему: {msg.text}")

    await state.set_state(TalkGPTFCM.step2)
    await InlineForm(msg= data_session.msg_talk_gpt,
                     main_text=data_session.msg_talk_gpt.md_text,
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    data_session.msg_talk_gpt = await InlineForm(msg=msg,
                     main_text=answer_str,
                     footer_text="",
                     keyboard=keyboard_collector.get_main_keyboard(prefix)).answer()

@router.message(F.text, TalkGPTFCM.step2)
async def cmd_dialog(msg : types.message, data_session_collector : DataSessionCollector):
    """Обработчик отвечает за ведение диалога"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)

    answer_str = data_session.gpt.get_answer(msg.text)

    await InlineForm(msg=data_session.msg_talk_gpt,
                     main_text=data_session.msg_talk_gpt.md_text,
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    data_session.msg_talk_gpt = data_session.msg_talk_gpt = await InlineForm(msg=msg,
                     main_text=answer_str,
                     footer_text="",
                     keyboard=keyboard_collector.get_main_keyboard(prefix)).answer()

