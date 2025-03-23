from itertools import count
from random import randint

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.ather.word import Word
from src.fsm.dictionary_fcm import DictionaryFCM as FCM
from src.gpt.dictionary_gpt import DictionaryGPT as GPT
from src.ather.data_session_collector import DataSessionCollector
from src.forms.inline_form import InlineForm
from src.keyboards import dictionary_keyboard
from src.keyboards.keyboard_collector import keyboard_collector
from src.ather.message_templates import message_templates
from src.ather.prefix import Prefix

prefix = Prefix.DICTIONARY.value  # %!% Поменяй в новом модуле

router = Router()
router.callback_query.filter(lambda clb: clb.data.startswith(prefix))


@router.callback_query(F.data.endswith("start"))
async def cmd_start(cbq: CallbackQuery, data_session_collector: DataSessionCollector):
    """Стартовый диалог работы со словарем"""
    data_session = data_session_collector.get_data_session(cbq.from_user.id)
    data_session.clear()
    data_session.gpt = GPT()

    await InlineForm(msg=cbq.message,
                     main_text=message_templates.get_start_message(Prefix.MAIN.value),
                     footer_text="*изучение слов*",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix),
                     is_md_txt=False).edit(separator=" ")

    data_session.msg_talk_gpt = await InlineForm(msg=cbq.message,
                                                 main_text=message_templates.get_start_message(prefix),
                                                 footer_text="",
                                                 keyboard=keyboard_collector.get_start_keyboard(prefix),
                                                 is_md_txt=False).answer()

@router.callback_query(F.data.endswith("add"))
async def cmd_add(cbq: CallbackQuery, state: FSMContext, data_session_collector: DataSessionCollector):
    """Запрашивает новое слово и предлагает ввести ответ на него
    """
    data_session = data_session_collector.get_data_session(cbq.from_user.id)

    await state.set_state(FCM.add)
    await InlineForm(msg=cbq.message,
                     main_text=cbq.message.md_text,
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    data_session.msg_talk_gpt = await InlineForm(msg=cbq.message,
                                                 main_text="Введите новое слово в формате английское слово\\перевод",
                                                 footer_text="",
                                                 keyboard=keyboard_collector.get_empty_keyboard(prefix),
                                                 is_md_txt=False).answer()


@router.callback_query(F.data.endswith("learn"))
async def cmd_learn(cbq: CallbackQuery, state: FSMContext, data_session_collector: DataSessionCollector):
    """Выводим новое слово на изучение
    """
    data_session = data_session_collector.get_data_session(cbq.from_user.id)

    await InlineForm(msg=cbq.message,
                     main_text=cbq.message.md_text,
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    await show_word(data_session, cbq.message, state)


@router.callback_query(F.data.endswith("show"))
async def cmd_show(cbq: CallbackQuery, data_session_collector: DataSessionCollector):
    """показывает слова, которые учим
    """
    data_session = data_session_collector.get_data_session(cbq.from_user.id)

    await InlineForm(msg=cbq.message,
                     main_text=cbq.message.md_text,
                     footer_text="",
                     keyboard=keyboard_collector.get_empty_keyboard(prefix)).edit()

    if len(data_session.dictionary) == 0:
        await InlineForm(msg=cbq.message,
                         main_text="Вы пока не добавили салова.",
                         footer_text="",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix),
                         is_md_txt=False).answer()
    else:
        await InlineForm(msg=cbq.message,
                         main_text="Вот что учим. Один блок не более 20 слов",
                         footer_text="",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix),
                         is_md_txt=False).answer()

        count_word = 50
        msg_word = ""
        for word in data_session.dictionary:

            msg_word += f"{word.text} : {word.translation}. Показано раз - {word.shows}, правильных ответов {word.answers}\n"
            count_word -= 1

            if count_word == 0:
                count_word = 50
                await InlineForm(msg=cbq.message,
                                 main_text=msg_word,
                                 footer_text="",
                                 keyboard=keyboard_collector.get_empty_keyboard(prefix),
                                 is_md_txt=False).answer()
                msg_word = ""

        if msg_word != "":
            await InlineForm(msg=cbq.message,
                             main_text=msg_word,
                             footer_text="",
                             keyboard=keyboard_collector.get_empty_keyboard(prefix),
                             is_md_txt=False).answer()

    data_session.msg_talk_gpt = await InlineForm(msg=cbq.message,
                                                 main_text=message_templates.get_start_message(prefix),
                                                 footer_text="",
                                                 keyboard=keyboard_collector.get_start_keyboard(prefix),
                                                 is_md_txt=False).answer()


@router.callback_query(F.data.endswith("end"))
async def cmd_end(cbq: types.CallbackQuery, state: FSMContext, data_session_collector: DataSessionCollector):
    """Прекращает работу со словарем"""
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


@router.message(F.text, FCM.add)
async def cmd_add_word(msg: types.message, state: FSMContext, data_session_collector: DataSessionCollector):
    """Обработчик отвечает за ввод нового слова"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)

    new_word_list = msg.text.split("\\")

    await state.clear()
    if len(new_word_list) == 2:

        new_word = Word(msg.from_user.id, new_word_list[0], new_word_list[1])
        data_session.dictionary.append(new_word)
        data_session.save_dictionary_word(new_word)
        await InlineForm(msg=data_session.msg_talk_gpt,
                         main_text="Слово добавлено к изучению",
                         footer_text=f"Слово: *{new_word_list[0]}*, перевод *{new_word_list[1]}*",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix),
                         is_md_txt=False).answer(separator="\n")

        data_session.msg_talk_gpt = await InlineForm(msg=msg,
                                                     main_text=message_templates.get_start_message(prefix),
                                                     footer_text="",
                                                     keyboard=keyboard_collector.get_start_keyboard(prefix),
                                                     is_md_txt=False).answer()
    else:

        await InlineForm(msg=data_session.msg_talk_gpt,
                         main_text="Кажется вы что то не тов ввели.",
                         footer_text=f"Слово: *{msg.text}*",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix),
                         is_md_txt=False).answer(separator="\n")

        data_session.msg_talk_gpt = await InlineForm(msg=msg,
                                                     main_text=message_templates.get_start_message(prefix),
                                                     footer_text="",
                                                     keyboard=keyboard_collector.get_start_keyboard(prefix),
                                                     is_md_txt=False).answer()


@router.message(F.text, FCM.learn)
async def cmd_learn_answer(msg: types.message, state: FSMContext, data_session_collector: DataSessionCollector):
    """Обработчик отвечает ответ на слово"""
    data_session = data_session_collector.get_data_session(msg.from_user.id)

    if data_session.current_word.translation.lower() == msg.text.lower():
        data_session.current_word.answers += 1
        data_session.update_word(data_session.current_word)

        await InlineForm(msg=data_session.msg_talk_gpt,
                         main_text="Верно!",
                         footer_text="",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix),
                         is_md_txt=False).answer(separator="\n")

    else:
        await InlineForm(msg=data_session.msg_talk_gpt,
                         main_text="Не верно! Правильный ответ:",
                         footer_text=f"{data_session.current_word.translation}",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix),
                         is_md_txt=False).answer(separator=" ")

    await show_word(data_session, msg, state)


async def show_word(data_session, msg, state):
    dictionary = data_session.dictionary

    if len(data_session.dictionary) == 0:

        await InlineForm(msg=msg,
                         main_text="Вы пока не добавили салова.",
                         footer_text="",
                         keyboard=keyboard_collector.get_empty_keyboard(prefix),
                         is_md_txt=False).answer()

        data_session.msg_talk_gpt = await InlineForm(msg=msg,
                                                     main_text=message_templates.get_start_message(prefix),
                                                     footer_text="",
                                                     keyboard=keyboard_collector.get_start_keyboard(prefix),
                                                     is_md_txt=False).answer()

    else:
        await state.set_state(FCM.learn)
        word = None
        if len(dictionary) == 1:
            word = dictionary[0]
        else:
            word = dictionary[randint(0, len(dictionary))]

        word.shows+=1
        data_session.update_word(word)

        data_session.current_word = word
        data_session.msg_talk_gpt = await InlineForm(msg=msg,
                                                     main_text="Введите перевод слова:",
                                                     footer_text=f"*{word.text}*",
                                                     keyboard=dictionary_keyboard.get_end_keyboard(),
                                                     is_md_txt=False).answer(separator=" ")
