import json

from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from src.ather.message_templates import message_templates
from src.ather.prefix import Prefix

import src.keyboards.quiz_keyboard as keyboard

from src.ather.data_session_collector import DataSessionCollector
from src.forms.inline_form import InlineForm

from src.fsm.talk_fp_gpt_fcm import TalkFPGPTFCM
from src.gpt.talk_gpt import TalkGPT
from src.keyboards.keyboard_collector import keyboard_collector

prefix = Prefix.TALK_FP.value #%!% Поменяй в новом модуле

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

    await state.set_state(TalkFPGPTFCM.step1)
    await InlineForm(msg= cbq.message,
                        main_text= cbq.message.md_text,
                        footer_text= "",
                        keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    data_session.msg_talk_gpt = await InlineForm(msg= cbq.message,
                    main_text= message_templates.get_start_message(prefix),
                    footer_text= message_templates.get_start_message_f(prefix),
                    keyboard= keyboard_collector.get_start_keyboard(prefix)).answer()

@router.callback_query(F.data.endswith(("_flint", "_bender", "_ioda")))
async def cmd_theme(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector):
    """Выбор темы в разговоре с gpt"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)

    answer_str = ""
    if cbq.data.endswith("_flint"):
        answer_str = data_session.gpt.get_answer("Поговори со мной от лица капитана Флинта")
    elif cbq.data.endswith("_bender"):
        answer_str = data_session.gpt.get_answer("Поговори со мной от лица робота Бендера из Футурамы")
    elif cbq.data.endswith("_ioda"):
        answer_str = data_session.gpt.get_answer("Поговори со мной от лица магистра Йоды из Звездных Войн")

    await state.set_state(TalkFPGPTFCM.step2)
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

@router.message(F.text, TalkFPGPTFCM.step1)
async def cmd_msg_theme(msg : types.message, state: FSMContext, data_session_collector : DataSessionCollector):
    """Обработчик отвечает за ввод личности
    В связи с ограничениями gpt мы не можем предоставить эту возможность"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)

    await state.set_state(TalkFPGPTFCM.step2)
    await InlineForm(msg= data_session.msg_talk_gpt,
                     main_text=data_session.msg_talk_gpt.md_text,
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    if msg.text.lower() in ("мастер йода", "бендер", "капитан Флинт"):

        dict_fm = {"мастер йода": "Магистр Йода из Звездных Войн",
                   "бендер": "Робот бендер из Футурамы",
                   "капитан флинт": "Капитан Флинт"}

        answer_str = data_session.gpt.get_answer(f"Поговори со мной от лица персонажа: {dict_fm.get(msg.text.lower())}")
        data_session.msg_talk_gpt = await InlineForm(msg=msg,
                                                     main_text=answer_str,
                                                     footer_text="",
                                                     keyboard=keyboard_collector.get_main_keyboard(prefix)).answer()

    else:
        await InlineForm(msg=msg,
                     main_text="Не смог до него дозвонится. Давайте поговорим с теми кто точно на связи?( в связи с ограничениями на выбор личности ботом выбор этих самых личностей ограничен)",
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).answer()

        data_session.msg_talk_gpt = await InlineForm(msg= msg,
                     main_text=message_templates.get_start_message(prefix),
                     footer_text=message_templates.get_start_message_f(prefix),
                     keyboard=keyboard_collector.get_start_keyboard(prefix)).answer()

@router.message(F.text, TalkFPGPTFCM.step2)
async def cmd_dialog(msg : types.message, data_session_collector : DataSessionCollector):
    """Обработчик отвечает за ведение диалога"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)

    answer_str = data_session.gpt.get_answer(msg.text)

    await InlineForm(msg=data_session.msg_talk_gpt,
                     main_text=data_session.msg_talk_gpt.md_text,
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    data_session.msg_talk_gpt = await InlineForm(msg=msg,
                     main_text=answer_str,
                     footer_text="",
                     keyboard=keyboard_collector.get_main_keyboard(prefix)).answer()

