import json

from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from src.ather.message_templates import message_templates
from src.ather.prefix import Prefix

import src.keyboards.quiz_keyboard as keyboard

from src.ather.data_session_collector import DataSessionCollector
from src.forms.inline_form import InlineForm

from src.fsm.job_fcm import JobFCM as FCM
from src.gpt.job_gpt import TalkGPT as GPT
from src.keyboards.keyboard_collector import keyboard_collector

prefix = Prefix.JOB.value  # %!% Поменяй в новом модуле

router = Router()
router.callback_query.filter(lambda clb: clb.data.startswith(prefix))


####################################################################################################
# Обработчики callback_query
####################################################################################################

@router.callback_query(F.data.endswith("start"))
async def cmd_start(cbq: types.CallbackQuery, state: FSMContext, data_session_collector: DataSessionCollector):
    """Стартовый диалог ввода информации по резюме"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)
    data_session.clear()
    data_session.gpt = GPT()

    await state.set_state(FCM.prof)
    await InlineForm(msg=cbq.message,
                     main_text= message_templates.get_start_message(Prefix.MAIN.value),
                     footer_text="*помощь с резюме*",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix),
                     is_md_txt=False).edit(separator=" ")

    data_session.msg_talk_gpt = await InlineForm(msg=cbq.message,
                                                 main_text="Начнем с вашего ФИО:",
                                                 footer_text="",
                                                 keyboard=keyboard_collector.get_start_keyboard(prefix),
                                                 is_md_txt=False).answer()

@router.callback_query(F.data.endswith("end"))
async def cmd_end(cbq: types.CallbackQuery, state: FSMContext, data_session_collector: DataSessionCollector):
    """Прекращает ввод резюме и переходит на главный экран"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)

    data_session.clear()
    await state.clear()
    await InlineForm(msg=cbq.message,
                     main_text=cbq.message.md_text,
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    await InlineForm(msg=cbq.message,
                     main_text=message_templates.get_start_message(Prefix.MAIN.value),
                     footer_text=message_templates.get_start_message_f(Prefix.MAIN.value),
                     keyboard=keyboard_collector.get_start_keyboard(Prefix.MAIN.value),
                     is_md_txt=False).answer()

####################################################################################################
# Обработчики message
####################################################################################################

@router.message(F.text, FCM.prof)
async def cmd_dialog_prof(msg: types.message, state: FSMContext, data_session_collector: DataSessionCollector):
    """Обработчик отвечает за ведение диалога"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)
    data_session.job["name"] = msg.text

    await state.set_state(FCM.salary)
    await InlineForm(msg=data_session.msg_talk_gpt,
                     main_text=data_session.msg_talk_gpt.text,
                     footer_text=f"*{msg.text}*",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit(separator=" ")

    data_session.msg_talk_gpt = await InlineForm(msg=msg,
                                                 main_text="Напишите вашу профессию:",
                                                 footer_text="",
                                                 keyboard=keyboard_collector.get_main_keyboard(prefix),
                                                 is_md_txt=False).answer()


@router.message(F.text, FCM.salary)
async def cmd_dialog_salary(msg: types.message, state: FSMContext, data_session_collector: DataSessionCollector):
    """Обработчик отвечает за ведение диалога"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)
    data_session.job["prof"] = msg.text

    await state.set_state(FCM.end)
    await InlineForm(msg=data_session.msg_talk_gpt,
                     main_text=data_session.msg_talk_gpt.md_text,
                     footer_text=f"*{msg.text}*",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit(separator=" ")

    data_session.msg_talk_gpt = await InlineForm(msg=msg,
                                                 main_text="Напишите вашу желаемую зарплату",
                                                 footer_text="",
                                                 keyboard=keyboard_collector.get_main_keyboard(prefix),
                                                 is_md_txt=False).answer()


@router.message(F.text, FCM.end)
async def cmd_dialog_end(msg: types.message, state: FSMContext, data_session_collector: DataSessionCollector):
    """Обработчик отвечает за ведение диалога"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)
    data_session.job["salary"] = msg.text

    await state.set_state(FCM.end)
    await InlineForm(msg=data_session.msg_talk_gpt,
                     main_text=data_session.msg_talk_gpt.md_text,
                     footer_text=f"*{msg.text}*",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit(separator=" ")

    answer_str = data_session.gpt.get_answer(f"Составь резюме по переданным данным: {str(data_session.job)}")
    data_session.msg_talk_gpt = await InlineForm(msg=msg,
                                                 main_text=answer_str,
                                                 footer_text="",
                                                 keyboard=keyboard_collector.get_empty_keyboard(prefix),
                                                 is_md_txt=False).answer()

    await InlineForm(msg=data_session.msg_talk_gpt,
                     main_text=message_templates.get_start_message(Prefix.MAIN.value),
                     footer_text=message_templates.get_start_message_f(Prefix.MAIN.value),
                     keyboard=keyboard_collector.get_start_keyboard(Prefix.MAIN.value),
                     is_md_txt=False).answer()
