import random
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from keyboards.anonims import keyboard_anonim
from models.user import User
from states.anonim_state import AnonimState
from aiogram.fsm.context import FSMContext

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
active_connections = {}
waiting_users = set()

@router.message(AnonimState.anonim_id)
async def handle_anonim_message(message: Message, state: FSMContext):
    # Bu yerda faqat anonim chat bo'limida ishlaydi
    pass

@router.message()
async def handle_non_anonim_message(message: Message, state: FSMContext):
    user_state = await state.get_state()
    if user_state != AnonimState.anonim_id:
        # Bu yerda anonim bo'limda bo'lmagan xabarlar ishlaydi
        receiver_id = active_connections.get(message.from_user.id)

        if receiver_id:
            try:
                await message.bot.send_message(chat_id=receiver_id, text=message.text)
            except Exception as e:
                await message.answer("<b>Xabar yuborishda xatolik yuz berdi.</b>")
        else:
            await message.answer("<b>Siz hali hech kim bilan ulanmagansiz.</b>")

@router.callback_query(F.data.startswith("accept_"))
async def accept_connection(callback: CallbackQuery, state: FSMContext):
    user_state = await state.get_state()
    if user_state == AnonimState.anonim_id:
        requester_id = int(callback.data.split("_")[1])
        responder_id = callback.from_user.id

        # Ulash jarayoni
        active_connections[requester_id] = responder_id
        active_connections[responder_id] = requester_id

        # Tasdiqlash haqida xabar berish
        await callback.message.edit_text("<b>Siz ulanishni tasdiqladingiz. Endi suhbatlashishingiz mumkin!</b>")
        await callback.bot.send_message(
            chat_id=requester_id,
            text="<b>Ulanish tasdiqlandi ✅. Endi suhbatni boshlashingiz mumkin!</b>"
        )

@router.callback_query(F.data.startswith("block_"))
async def block_connection(callback: CallbackQuery):
    requester_id = int(callback.data.split("_")[1])  # The ID of the requester (initiator of the connection)

    # Send rejection message to the requester
    try:
        await callback.bot.send_message(
            chat_id=requester_id,
            text="<b>Foydalanuvchi siz bilan suhbatlashishni rad etdi.</b>"
        )
    except Exception as e:
        await callback.message.answer("<b>Rad etilganligi haqida xabar yuborishda xatolik yuz berdi.</b>")

    # Update callback message text
    await callback.message.edit_text("<b>Siz ulanishni rad etdingiz.</b>")

    # Disconnect users
    responder_id = callback.from_user.id  # The ID of the responder (the one who blocked the request)

    if requester_id in active_connections:
        del active_connections[requester_id]
    if responder_id in active_connections:
        del active_connections[responder_id]

    # Remove both users from the waiting queue if they are there
    if requester_id in waiting_users:
        waiting_users.remove(requester_id)
    if responder_id in waiting_users:
        waiting_users.remove(responder_id)

@router.callback_query(F.data == "exit_anonim")
async def exit_anonim(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("<b>Anonim bo'limdan chiqdingiz.</b>")

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
        await callback.bot.send_message(chat_id=partner_id, text="<b>Random foydalanuvchi topildi ✅ Endi yozishingiz mumkin!</b>")
    else:
        # Navbatga qo‘shish
        waiting_users.add(user_id)
        await callback.message.answer("<b>Random foydalanuvchi topilmoqda, iltimos kuting...</b>")


@router.message()
async def handle_non_anonim_message(message: Message, state: FSMContext):
    # Foydalanuvchining hozirgi holatini olish
    user_state = await state.get_state()

    # Foydalanuvchi anonim holatda emasligini tekshirish
    if user_state != AnonimState.anonim_id:
        # Agar foydalanuvchi anonim holatda bo'lmasa
        receiver_id = active_connections.get(message.from_user.id)

        # Agar foydalanuvchi hali hech kim bilan ulanmagan bo'lsa
        if not receiver_id:
            await message.answer("<b>Siz hali hech kim bilan ulanmagansiz.</b>")
        else:
            # Agar foydalanuvchi ulanishda bo'lsa, xabarni yuborish
            try:
                await message.bot.send_message(chat_id=receiver_id, text=message.text)
            except Exception as e:
                await message.answer("<b>Xabar yuborishda xatolik yuz berdi.</b>")
    else:
        # Agar foydalanuvchi anonim holatda bo'lsa, uning xabarini yuborish
        receiver_id = active_connections.get(message.from_user.id)
        if receiver_id:
            try:
                await message.bot.send_message(chat_id=receiver_id, text=message.text)
            except Exception as e:
                await message.answer("<b>Xabar yuborishda xatolik yuz berdi.</b>")
        else:
            await message.answer("<b>Siz hali hech kim bilan ulanmagansiz.</b>")
