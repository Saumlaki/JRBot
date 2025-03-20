
from aiogram import Router, types, F
from aiogram.types import CallbackQuery

from src.forms.inline_form import InlineForm
from src.keyboards.keyboard_collector import keyboard_collector
from src.ather.message_templates import message_templates
from src.ather.prefix import Prefix


prefix = Prefix.DICTIONARY.value #%!% Поменяй в новом модуле

router = Router()
router.message.filter(lambda msg : msg.text.startswith(prefix))
router.callback_query.filter(lambda clb : clb.data.startswith(prefix))


@router.callback_query(F.data.endswith("start"))
async def cmd_start(cbq : CallbackQuery):
    """Стартовый диалог работы со словарем"""
    await InlineForm(msg= cbq.message,
                    main_text= cbq.message.text,
                    footer_text= "",
                    keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    await InlineForm(msg= cbq.message,
                    main_text= message_templates.get_start_message(prefix),
                    footer_text= message_templates.get_start_message_f(prefix),
                    keyboard= keyboard_collector.get_start_keyboard(prefix)).answer()

@router.callback_query(F.data.endswith("next"))
async def cmd_next(cbq : CallbackQuery):
    """Запрашивает новое слово и предлагает ввести ответ на него
    """
    await InlineForm(msg= cbq.message,
                    main_text= cbq.message.text,
                    footer_text= "",
                    keyboard= keyboard_collector.get_empty_keyboard(prefix)).edit()

    await InlineForm(msg= cbq.message,
                    main_text= message_templates.get_add_message(prefix),
                    footer_text= message_templates.get_add_message_f(prefix),
                    keyboard= keyboard_collector.get_add_keyboard(prefix)).answer()














    # [types.InlineKeyboardButton(text="Выучить новое слово", callback_data=f"{prefix}next"),
    #  types.InlineKeyboardButton(text="Повторить то выучил ранее", callback_data=f"{prefix}repeat"),
    #  types.InlineKeyboardButton(text="Повторить трудные", callback_data=f"{prefix}repeat_difficult")]














        #data_helper_collector.get_data_helper(cbq.id).get_main_message())
   # .get_main_message())
    #cbq.answer(f"Джага1")


# @router.message(F.text)
# async def cmd_start_dict(message: types.Message):
#     await message.answer(f"Джага2")


@router.message(F.text)
async def cmd_start(message: types.Message):
    print(message.text.endswith("start"))
    await message.answer(f"qqqqqqqq")