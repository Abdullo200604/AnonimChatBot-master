from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

keyboard_anonim = InlineKeyboardBuilder()
keyboard_anonim.row(types.InlineKeyboardButton(text="👤 ID orqali ulanish", callback_data="connect_id"), types.InlineKeyboardButton(text="🥷 Random ulanish", callback_data="connect_random"))
keyboard_anonim.row(types.InlineKeyboardButton(text="Orqaga 🔙", callback_data="back"))


keyboard_anonim_back = InlineKeyboardBuilder()
keyboard_anonim_back.row(types.InlineKeyboardButton(text="Orqaga 🔙", callback_data="back"))

