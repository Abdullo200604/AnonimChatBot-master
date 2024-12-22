import base64
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from keyboards.encryptions import keyboard_encryption, keyboard_encryption_back
from states.encyption import Encryption, Decryption
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data == "shifr")
async def cmd_shifr(callback: CallbackQuery):
    await callback.message.edit_text("<b>Tanlang:</b>", reply_markup=keyboard_encryption.as_markup())


@router.callback_query(F.data == "encryption")
async def cmd_encryption(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("<b>Shifrlash matnini kiriting:</b>")
    await state.set_state(Encryption.encrypt_text)


@router.message(Encryption.encrypt_text)
async def encrypt_text(message: Message, state: FSMContext):
    await state.update_data(encrypt_text=message.text)
    data = await state.get_data()
    await state.clear()
    encrypt_text = data.get("encrypt_text", "Unknown")
    encrypted_text = base64.b64encode(encrypt_text.encode('utf-8')).decode('utf-8')
    await message.answer(f"<b>Tayyor ✅\nShifrlangan matn:<code>{encrypted_text}</code></b>",
                            reply_markup=keyboard_encryption_back.as_markup())


@router.callback_query(F.data == "decryption")
async def cmd_decryption(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("<b>Shifrdan chiqarish matnini kiriting:</b>")
    await state.set_state(Decryption.decrypt_text)


@router.message(Decryption.decrypt_text)
async def decrypt_text(message: Message, state: FSMContext):
    await state.update_data(decrypt_text=message.text)
    data = await state.get_data()
    await state.clear()
    decrypt_text = data.get("decrypt_text", "Unknown")
    decrypted_text = base64.b64decode(decrypt_text).decode('utf-8')
    await message.answer(f"<b>Tayyor ✅\nShifrdan chiqarilgan matn:<code>{decrypted_text}</code></b>",
                                reply_markup=keyboard_encryption_back.as_markup())
