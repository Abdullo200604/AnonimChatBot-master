from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

keyboard_encryption = InlineKeyboardBuilder()
keyboard_encryption.row(types.InlineKeyboardButton(text="🔐 Shifrlash", callback_data="encryption"), types.InlineKeyboardButton(text="🔓 Shifrni yechish", callback_data="decryption"))
keyboard_encryption.row(types.InlineKeyboardButton(text="Orqaga 🔙", callback_data="back"))


keyboard_encryption_back = InlineKeyboardBuilder()
keyboard_encryption_back.row(types.InlineKeyboardButton(text="Orqaga 🔙", callback_data="back"))