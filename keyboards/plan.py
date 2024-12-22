from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models.plan import Plan

keyboard_plan = InlineKeyboardBuilder()
keyboard_plan.row(types.InlineKeyboardButton(text="Reja qo'shish 📝", callback_data="plan_add"), types.InlineKeyboardButton(text="Reja o'chirish 🗑", callback_data="plan_remove"))
keyboard_plan.row(types.InlineKeyboardButton(text="Orqaga 🔙", callback_data="back"),types.InlineKeyboardButton(text="Reja ko'rish 📋", callback_data="plan_see"))


unnecessary = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Kerak emas")]
], resize_keyboard=True)


async def remove_plan_buttons():
    keyboard_plan_remove = InlineKeyboardBuilder()
    plans = await Plan.all()
    for plan in plans:
        keyboard_plan_remove.row(types.InlineKeyboardButton(text=f"{plan.id}. {plan.plan_time}: {plan.plan_text}", callback_data=f"remove_plan_{plan.id}"))

    return keyboard_plan_remove.as_markup()