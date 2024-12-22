from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.randoms import keyboard_random
from random import randint
from models import data
from keyboards.randoms import keyboard_random_back

router = Router()


@router.callback_query(F.data == "tasodif")
async def cmd_start(callback: CallbackQuery):
    await callback.message.edit_text("<b>Tanlang:</b>", reply_markup=keyboard_random.as_markup())


@router.callback_query(F.data == "random_tasks")
async def cmd_random_tasks(callback: CallbackQuery):
    random_number = randint(1, 50)
    await callback.message.edit_text(f"<b>📋 Topshiriq: <i>{data.data_tasks[random_number]}</i></b>",
                                     reply_markup=keyboard_random_back.as_markup())

@router.callback_query(F.data == "random_facts")
async def cmd_random_facts(callback: CallbackQuery):
    random_number = randint(1, 50)
    await callback.message.edit_text(f"<b>🤓 Faktlar: <i>{data.data_facts[random_number]}</i></b>",
                                     reply_markup=keyboard_random_back.as_markup())
