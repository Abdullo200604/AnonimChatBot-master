import random
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from keyboards.anonims import keyboard_anonim
from models.user import User
from states.anonim_state import AnonimState
from aiogram.fsm.context import FSMContext

router = Router()
active_connections = {}
waiting_users = set()


@router.callback_query(F.data == "anonim")
async def anonim_stage(callback: CallbackQuery):
    await callback.message.edit_text("<b>Tanlang: </b>", reply_markup=keyboard_anonim.as_markup())


@router.callback_query(F.data == "connect_id")
async def anonim_id_connect(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("<b>Id kiriting:</b>")
    await state.set_state(AnonimState.anonim_id)


@router.message(AnonimState.anonim_id)
async def update_anonim_id(message: Message, state: FSMContext):
    await state.update_data(anonim_id=message.text)
    data = await state.get_data()
    user_id = data.get("anonim_id", "Unknown")
    user_id_check = await User.get_or_none(user_id=user_id)

    if user_id_check:
        active_connections[message.from_user.id] = user_id_check.user_id
        active_connections[user_id_check.user_id] = message.from_user.id

        await message.answer("<b>Ulanmoqda....</b>")
        await message.answer("<b>Ulandi ✅ Endi yozishingiz mumkin!</b>")
        await state.clear()
    else:
        await message.answer("<b>Bunday foydalanuvchi mavjud emas.</b>")
        await state.clear()


@router.callback_query(F.data == "connect_random")
async def random_button(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id in waiting_users:
        await callback.answer("Siz allaqachon navbatdasiz.", show_alert=True)
        return

    # Agar navbatda boshqa foydalanuvchi bo‘lsa
    if waiting_users:
        partner_id = waiting_users.pop()
        active_connections[user_id] = partner_id
        active_connections[partner_id] = user_id

        await callback.message.answer("<b>Random foydalanuvchi topildi ✅ Endi yozishingiz mumkin!</b>")
        await router.bot.send_message(chat_id=partner_id, text="<b>Random foydalanuvchi topildi ✅ Endi yozishingiz mumkin!</b>")
    else:
        # Navbatga qo‘shish
        waiting_users.add(user_id)
        await callback.message.answer("<b>Random foydalanuvchi topilmoqda, iltimos kuting...</b>")


@router.message(F.text)
async def handle_messages(message: Message, bot: Bot):
    receiver_id = active_connections.get(message.from_user.id)

    if receiver_id:
        try:
            await bot.send_message(chat_id=int(receiver_id), text=message.text)
        except Exception as e:
            await message.answer("<b>Xabar yuborishda xatolik yuz berdi.</b>")
    else:
        await message.answer("<b>Siz hali hech kim bilan ulanmagansiz.</b>")