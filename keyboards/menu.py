from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

keyboard = InlineKeyboardBuilder()
keyboard.row(types.InlineKeyboardButton(text="📋 Rejalar bilan ishlash", callback_data="reja"), types.InlineKeyboardButton(text="🎲 Tasodifiy", callback_data="tasodif"))
keyboard.row(types.InlineKeyboardButton(text="🔐 Shifrlash", callback_data="shifr"), types.InlineKeyboardButton(text="👥 Anonim Chat", callback_data="anonim"))