import json

from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from src.ather.message_templates import message_templates
from src.ather.prefix import Prefix

import src.keyboards.quiz_keyboard as keyboard
from src.ather.data_session_collector import DataSessionCollector
from src.forms.inline_form import InlineForm

from src.fsm.quiz_fcm import QuizFCM
from src.gpt.quiz_gpt import QuizGPT
from src.keyboards.keyboard_collector import keyboard_collector

prefix = Prefix.QUIZ.value #%!% Поменяй в новом модуле

router = Router()
router.callback_query.filter(lambda clb : clb.data.startswith(prefix))

####################################################################################################
# Обработчики callback_query
####################################################################################################

@router.callback_query(F.data.endswith("start"))
async def cmd_start(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector):
    """Стартовый диалог игры в квиз"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)
    data_session.gpt= QuizGPT()

    await state.set_state(QuizFCM.choosing_theme)
    await InlineForm(msg= cbq.message,
                        main_text= cbq.message.md_text.split("\n\n")[0],
                        footer_text= "",
                        keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    await InlineForm(msg= cbq.message,
                    main_text= message_templates.get_start_message(prefix),
                    footer_text= message_templates.get_start_message_f(prefix),
                    keyboard= keyboard_collector.get_start_keyboard(prefix)).answer()

@router.callback_query(F.data.endswith(('_theme_animals', '_theme_fish', '_theme_plants', '_theme_space', '_theme_earth', '_theme_any')))
async def cmd_theme(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector, ):
    """Выбор темы в квизе"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)

    if cbq.data.endswith("_theme_animals"):
        data_session.gpt.set_theme("Тема: животные")
    elif cbq.data.endswith("_theme_fish"):
        data_session.gpt.set_theme("Тема: рыбы")
    elif cbq.data.endswith("_theme_plants"):
        data_session.gpt.set_theme("Тема: растения")
    elif cbq.data.endswith("_theme_space"):
        data_session.gpt.set_theme("Тема: космос")
    elif cbq.data.endswith("_theme_earth"):
        data_session.gpt.set_theme("Тема: наша планета")
    elif cbq.data.endswith("_theme_any"):
        data_session.gpt.set_theme("Тема: любая тема")

    answer_dict = get_answer(data_session.gpt)

    data_session.quiz_answers = answer_dict["Решение"]
    data_session.quiz_count+=1
    await state.set_state(QuizFCM.selected_theme)
    await InlineForm(msg= cbq.message,
                        main_text= cbq.message.md_text.split("\n\n")[0],
                        footer_text= "",
                        keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()
    data_session.msg_talk_gpt = await InlineForm(msg=cbq.message,
                     main_text=answer_dict["Вопрос"],
                     footer_text="",
                     keyboard=keyboard.get_main_keyboard(answer_dict["Ответы"])).answer()

@router.callback_query(F.data.startswith(f"{prefix}_answer_") )
async def cmd_answer(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector, ):
    """Выбор ответа"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)
    answer = cbq.data.split("_")[-1]

    if answer.lower() == data_session.quiz_answers.lower():
        footer_text = f"_Вы ответили правильно:_ *{answer.lower()}*"
        data_session.quiz_results += 1
    else:
        footer_text = f"_Вы ответили не правильно: {answer.lower()}\nПравильный ответ:_ *{data_session.quiz_answers.lower()}*"

    await InlineForm(msg= cbq.message,
                        main_text= cbq.message.md_text.split("\n\n")[0],
                        footer_text= footer_text,
                        keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    answer_dict = get_answer(data_session.gpt)

    data_session.quiz_answers = answer_dict["Решение"]
    data_session.quiz_count += 1

    data_session.msg_talk_gpt = await InlineForm(msg=cbq.message,
                     main_text=answer_dict["Вопрос"],
                     footer_text="",
                     keyboard=keyboard.get_main_keyboard(answer_dict["Ответы"])).answer()

@router.callback_query(F.data.endswith("end"))
async def cmd_end(cbq : types.CallbackQuery, state: FSMContext, data_session_collector : DataSessionCollector):
    """Прекращает игру в квиз"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)

    data_session.quiz_answers = ""
    data_session.msg_talk_gpt = None
    await state.clear()
    await InlineForm(msg=cbq.message,
                     main_text= cbq.message.md_text.split("\n\n")[0],
                     footer_text= "",
                     keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    if data_session.quiz_count == 0:
        await InlineForm(msg=cbq.message,
                         main_text=f"Нет вопросов, нет ответов. Приходи поиграть еще",
                         footer_text="",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix)).answer()
    elif  data_session.quiz_results == 0:
        await InlineForm(msg=cbq.message,
                         main_text=f"Ни одного правильного ответа! Вот ото результат! Но не стоит им хвастаться",
                         footer_text="",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix)).answer()
    elif data_session.quiz_count / data_session.quiz_results:
        await InlineForm(msg=cbq.message,
                         main_text=f"Слабовато. Надо потренироваться еще",
                         footer_text=f"_Вопросов: {data_session.quiz_count}, Ответы: {data_session.quiz_results}, Процент правильных ответов: {round(data_session.quiz_results / data_session.quiz_count * 100)}_",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix)).answer()
    else:
        await InlineForm(msg=cbq.message,
                         main_text=f"Круто. Ты умеешь делать квизы!",
                         footer_text=f"_Вопросов: {data_session.quiz_count}, Ответы: {data_session.quiz_results}, Процент правильных ответов: {round(data_session.quiz_results / data_session.quiz_count  * 100)}_",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix)).answer()


    await InlineForm(msg= cbq.message,
                    main_text= message_templates.get_start_message(Prefix.MAIN.value),
                    footer_text= message_templates.get_start_message_f(Prefix.MAIN.value),
                    keyboard= keyboard_collector.get_start_keyboard(Prefix.MAIN.value)).answer()

####################################################################################################
# Обработчики message
####################################################################################################

@router.message(F.text, QuizFCM.choosing_theme)
async def cmd_msg_theme(msg : types.message, state: FSMContext, data_session_collector : DataSessionCollector):
    """Обработчик отвечает за ввод произвольной темы квиза"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)
    data_session.gpt.set_theme(msg.text)

    answer_dict = get_answer(data_session.gpt)

    await state.set_state(QuizFCM.selected_theme)
    data_session.msg_talk_gpt = await InlineForm(msg= msg,
                        main_text= answer_dict["Вопрос"],
                        footer_text= "",
                        keyboard= keyboard.get_main_keyboard(answer_dict["Ответы"])).answer()

@router.message(F.text, QuizFCM.selected_theme)
async def cmd_msg_answer(msg : types.message, data_session_collector : DataSessionCollector):
    """Обработчик отвечает за ввод произвольного ответа квиза"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)

    answer = msg.text

    if answer.lower() == data_session.quiz_answers.lower():
        footer_text = f"_Вы ответили правильно:_ *{answer.lower()}*"
        data_session.quiz_results += 1
    else:
        footer_text = f"_Вы ответили не правильно: {answer.lower()}\nПравильный ответ:_ *{data_session.quiz_answers.lower()}*"


    await InlineForm(msg= data_session.msg_talk_gpt,
                     main_text=data_session.msg_talk_gpt.md_text.split("\n\n")[0],
                     footer_text=footer_text,
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    answer_dict = get_answer(data_session.gpt)

    data_session.quiz_answers = answer_dict["Решение"]
    data_session.quiz_count += 1

    data_session.msg_talk_gpt = await InlineForm(msg=msg,
                     main_text=answer_dict["Вопрос"],
                     footer_text="",
                     keyboard=keyboard.get_main_keyboard(answer_dict["Ответы"])).answer()

def get_answer(gpt):
    """ГПТ периодически тупит и возвращает кривую структуру ответа.
    Добьемся нормального ответа"""
    is_true = False
    while not is_true:
        answer_json = gpt.get_answer("Следующий вопрос")
        answer_dict = json.loads(answer_json)

        is_true = ("Решение" in answer_dict.keys() and "Вопрос" in answer_dict.keys() and "Ответы" in answer_dict.keys())
    return answer_dict

