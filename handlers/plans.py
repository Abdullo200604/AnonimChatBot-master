from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.plan import keyboard_plan, unnecessary, remove_plan_buttons
from aiogram import Bot
from states.plan import PlanAdd
from keyboards.menu import keyboard
from aiogram.fsm.context import FSMContext
from services.plan import add_plan
from models.plan import Plan

router = Router()

@router.callback_query(F.data == "reja")
async def cmd_plan(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text("<b>Kerakli tugmani tanlang: </b>", callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=keyboard_plan.as_markup())


@router.callback_query(F.data == "back")
async def cmd_back(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text("<b>Bosh Menyuga qaytildi ✅\nKerakli kategoriyani tanlang:</b>",
                                callback.message.chat.id, callback.message.message_id,
                                reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "plan_add")
async def cmd_plan_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("<b>Rejani kiriting: </b>")
    await state.set_state(PlanAdd.plan_text)


@router.message(PlanAdd.plan_text)
async def cmd_plan_text_update(message: Message, state: FSMContext):
    await state.update_data(plan_text=message.text)
    await message.answer(
        "<b>Rejani bajarish vaqtini kiriting (Ixtiyoriy):\nShablon: 06:00-08:00, Kerak emas tugmasini bosing!. </b>",
        reply_markup=unnecessary)
    await state.set_state(PlanAdd.plan_time)


@router.message(PlanAdd.plan_time)
async def cmd_plan_time_update(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(plan_time=message.text)
    del_mes = await message.answer("<b>Reja saqlanmoqda.... </b>", reply_markup=ReplyKeyboardRemove())
    await state.set_state(PlanAdd.finish)
    data = await state.get_data()
    await state.clear()
    plan_text = data.get("plan_text", "Unknown")
    plan_time = data.get("plan_time", "Unknown")
    await add_plan(user_id=message.chat.id, plan_text=plan_text, plan_time=plan_time)
    await message.answer("<b>Reja muvaffaqiyatli saqlandi ✅.</b>", reply_markup=keyboard.as_markup())
    await bot.delete_message(chat_id=message.chat.id, message_id=del_mes.message_id)


@router.callback_query(F.data == "plan_remove")
async def cmd_plan_remove(callback: CallbackQuery):
    plans = await Plan.all().count()
    if plans:
        await callback.message.edit_text("<b>O'chirish uchun rejani tanlang:</b>",
                                      reply_markup=await remove_plan_buttons())
    elif plans == 0:
        await callback.message.edit_text("<b>O'chirish uchun rejalar mavjud emas</b>", reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "plan_see")
async def cmd_plan_see(callback: CallbackQuery):
    plans = await Plan.all()
    plan_count = await Plan.all().count()
    if plans:
        text = "<b>Saqlangan rejalar:</b>\n"
        for plan in plans:
            text += f"{plan.id}. {plan.plan_time}: {plan.plan_text}\n"
        await callback.message.edit_text(text, reply_markup=keyboard_plan.as_markup())
        print(plan_count)
    elif plan_count == 0:
        await callback.message.edit_text("<b>Saqlangan rejalar yo'q.</b>", reply_markup=keyboard_plan.as_markup())




@router.callback_query()
async def cmd_remove_plan_process(callback: CallbackQuery):
    if callback.data.startswith("remove_plan_"):
        plan_id = int(callback.data.split('_')[2])
        plan = await Plan.get(id=plan_id)
        await plan.delete()
        await callback.message.edit_text(f"<b>Reja {plan.id}. {plan.plan_time}: {plan.plan_text} o'chirildi ✅.</b>",
                                         reply_markup=keyboard.as_markup())
        await plan.save()

