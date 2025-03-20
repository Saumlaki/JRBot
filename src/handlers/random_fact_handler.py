from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.ather.data_session_collector import DataSessionCollector
from src.ather.prefix import Prefix
from src.ather.message_templates import message_templates
from src.fsm.random_fact_fcm import RandomFactFCM
from src.gpt.random_fact_gpt import RandomFactGPT
from src.keyboards.keyboard_collector import keyboard_collector
from src.forms.inline_form import InlineForm


prefix = Prefix.RANDOM_FACT.value #%!% Поменяй в новом модуле

router = Router()
router.callback_query.filter(lambda clb : clb.data.startswith(prefix))

####################################################################################################
# Обработчики callback_query
####################################################################################################

@router.callback_query(F.data.endswith("start"))
async def cmd_start(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector):
    """Стартовый диалог работы со случайными фактами"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)
    data_session.gpt= RandomFactGPT()

    await state.set_state(RandomFactFCM.choosing_theme)
    await InlineForm(msg= cbq.message,
                        main_text= cbq.message.md_text.split("\n\n")[0],
                        footer_text= "",
                        keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    data_session.msg_talk_gpt = await InlineForm(msg= cbq.message,
                    main_text= message_templates.get_start_message(prefix),
                    footer_text= message_templates.get_start_message_f(prefix),
                    keyboard= keyboard_collector.get_start_keyboard(prefix)).answer()

@router.callback_query(F.data.endswith("next"))
async def cmd_next(cbq : types.CallbackQuery, data_session_collector : DataSessionCollector):
    """Выводит пользователю новый факт"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)
    data_session.random_fact_num+= 1

    await InlineForm(msg= cbq.message,
                        main_text= cbq.message.md_text.split("\n\n")[0],
                        footer_text= "",
                        keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    await InlineForm(msg= cbq.message,
                        main_text= data_session.gpt.get_answer("Следующий факт"),
                        footer_text= f"__Вы узнали фактов: {data_session.random_fact_num}__",
                        keyboard= keyboard_collector.get_main_keyboard(prefix)).answer()

@router.callback_query(F.data.endswith("end"))
async def cmd_end(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector):
    """Прекращает вывод фактов и переходит на главный экран"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)

    await state.clear()
    await InlineForm(msg=cbq.message,
                     main_text= cbq.message.md_text.split("\n\n")[0],
                     footer_text= "",
                     keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    await InlineForm(msg=cbq.message,
                     main_text= f"Я надеюсь что ты стал умнее. Сегодня ты узнал новых фактов: {data_session.random_fact_num}",
                     footer_text= "",
                     keyboard=  keyboard_collector.get_empty_keyboard(prefix)).answer()

    await InlineForm(msg= cbq.message,
                    main_text= message_templates.get_start_message(Prefix.MAIN.value),
                    footer_text= message_templates.get_start_message_f(Prefix.MAIN.value),
                    keyboard= keyboard_collector.get_start_keyboard(Prefix.MAIN.value)).answer()

####################################################################################################
# Обработчики message
####################################################################################################

@router.message(F.text, RandomFactFCM.choosing_theme)
async def cmd_choosing_theme(msg : types.message, state: FSMContext, data_session_collector : DataSessionCollector):
    """Обработчик отвечает за ввод произвольной темы интересных фактов"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)
    data_session.random_fact_num+= 1

    data_session.gpt.set_theme(msg.text)

    await state.set_state(RandomFactFCM.selected_theme)
    await InlineForm(msg=data_session.msg_talk_gpt,
                     main_text=data_session.msg_talk_gpt.md_text.split("\n\n")[0],
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    await InlineForm(msg= msg,
                        main_text= data_session.gpt.get_answer("Следующий факт"),
                        footer_text= f"Вы узнали фактов: {data_session.random_fact_num}",
                        keyboard= keyboard_collector.get_main_keyboard(prefix)).answer()