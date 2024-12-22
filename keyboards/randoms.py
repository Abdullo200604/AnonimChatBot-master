from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

keyboard_random = InlineKeyboardBuilder()
keyboard_random.row(types.InlineKeyboardButton(text="📋 Topshiriq", callback_data="random_tasks"), types.InlineKeyboardButton(text="🤓 Faktlar", callback_data="random_facts"))


keyboard_random_back = InlineKeyboardBuilder()
keyboard_random_back.row(types.InlineKeyboardButton(text="Orqaga 🔙", callback_data="back"))