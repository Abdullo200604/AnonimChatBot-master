from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from models.user import User
from services.user import add_user
from keyboards.menu import keyboard
router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    user = await User.get_or_none(user_id=message.from_user.id)
    if not user:
        await add_user(user_id=message.from_user.id, full_name=message.from_user.full_name, username=message.from_user.username)
        await message.answer(f"""<b>Assalomu Aleykum, {message.from_user.mention_html()}! 🌟

O'z-o'zini rivojlantirish botiga xush kelibsiz! 🎉

Sizning hayotingizda o'zgarish qilishga tayyor ekanligingizni ko'rib turibmiz! Siz bizning botimizga qo'shilish orqali yangi imkoniyatlar sari birinchi qadamni qo'ydingiz. Endi sizni yanada kuchliroq, baxtliroq va muvaffaqiyatliroq bo'lishga yo'naltiradigan barcha imkoniyatlar kutmoqda! 🚀💫

⚙️ Botimizda mavjud asosiy funksiyalar:

  1. Anonim chat 💬
     O'zingizni erkin his qilgan holda fikr almashing va haqiqiy his-tuyg'ularingizni ifoda eting.

  2. Shifrlash 🔐
     Maxfiylik siz uchun muhim! Ma'lumotlaringiz to'liq xavfsiz.

  3. Tasodifiy maslahatlar 🎲
     Har kuni yangi ilhom beruvchi fikrlar va motivatsion maslahatlar.

  4. Reja bilan ishlash 📅
     Kichik qadamlar, katta o'zgarishlarga olib keladi. O'z maqsadlaringizni rejalashtiring va amalga oshirish yo'lida har kuni yangi imkoniyatlar yaratib boring!</b>


""",reply_markup=keyboard.as_markup())

    else:
        await message.answer(f"""<b>Qaytganingiz bilan, {message.from_user.mention_html()}! 🌟

Bizni yana tanlaganingizdan xursandmiz! 🎉 Bu safar sizni yangi imkoniyatlar, yangi motivatsiya va hayotingizni o'zgartirishga undaydigan yangi resurslar kutmoqda! Siz hozirgacha o'zingizni rivojlantirish yo'lida katta qadamlar tashladingiz, endi esa yanada katta yutuqlarga erishish vaqti keldi. 🚀

⚙️ Botimizda sizni kutayotgan yangi imkoniyatlar:

    Anonim chat 💬
    Fikrlaringizni erkin tarzda baham ko'ring. Endi hech narsa to'sqinlik qilmaydi!

    Shifrlash 🔐
    Maxfiylikni ta'minlash bizning ustuvorligimizdir. Ma'lumotlaringiz xavfsiz bo'lishi kerak!

    Tasodifiy maslahatlar 🎲
    Yangi ilhom olish uchun har kuni tasodifiy motivatsion maslahatlar. Sizga kerakli bo'lgan qo'llab-quvvatlashni toping!

    Reja bilan ishlash 📅
    O'z maqsadlaringizni aniq rejalashtiring va har kuni ularga bir qadam yaqinlashish uchun harakat qiling.


</b>""",reply_markup=keyboard.as_markup())


@router.message(Command('help'))
async def cmd_help(message: Message):
    help_text = (
        "<b>Botdan foydalanish bo'yicha batafsil ma'lumot:</b>\n\n"
        "Asosiy buyruqlar:\n"
        "/start - Botni ishga tushiradi va asosiy menyuni ko'rsatadi.\n"
        "/help - Botdan foydalanish bo'yicha yordam beradi.\n"
        "/info - Botning imkoniyatlari va funksiyalari haqida ma'lumot beradi.\n\n"

        "Asosiy menyu imkoniyatlari:\n"
        "📋 Rejalar bilan ishlash:\n"
        " - Rejalarni ko'rish: Foydalanuvchining saqlangan rejalarini ko'rsatadi.\n"
        " - Reja qo'shish: Yangi reja kiritish imkonini beradi.\n"
        " - Rejani o'chirish: Tanlangan rejani ro'yxatdan o'chiradi.\n\n"

        "🎲 Tasodifiy:\n"
        " - Tasodifiy topshiriq: Foydali kunlik topshiriq taklif etadi.\n"
        " - Tasodifiy fakt: Qiziqarli yoki rivojlanishga oid fakt ko'rsatadi.\n\n"

        "🔐 Shifrlash:\n"
        " - Matnni shifrlash: Foydalanuvchidan matnni so'raydi, base64 formatida shifrlab, qaytaradi.\n"
        " - Shifrni yechish: Base64 formatidagi matnni ochib, asl holiga qaytaradi.\n\n"

        "👥 Anonim Chat:\n"
        " - Random chat: Foydalanuvchini tasodifiy boshqa foydalanuvchi bilan ulaydi.\n"
        " - ID orqali chat: Tanlangan IDga ulanish imkoniyatini beradi.\n\n"

        "Foydalanuvchi xavfsizligi:\n"
        " - Anonim chatda foydalanuvchilarni IDlari orqali nazorat qilish va bloklash."
    )
    await message.answer(help_text, reply_markup=keyboard.as_markup())


@router.message(Command('info'))
async def cmd_info(message: Message):
    info_text = (
        "<b>Botning imkoniyatlari va funksiyalari:</b>\n\n"
        "Bu bot foydalanuvchilarga turli vazifalarni bajarishda yordam beradi.\n\n"

        "Asosiy funktsiyalar:\n"
        "- Rejalar bilan ishlash: Foydalanuvchilar o'z rejalarini ko'rish, qo'shish yoki o'chirish imkoniga ega.\n"
        "- Tasodifiy topshiriqlar va faktlar: Bot foydalanuvchiga har kuni foydali topshiriqlar yoki qiziqarli faktlar taklif etadi.\n"
        "- Shifrlash va shifrlashni yechish: Matnlarni base64 formatida shifrlash va yechish imkoniyati.\n"
        "- Anonim chat: Foydalanuvchilarni tasodifiy yoki ID orqali anonim tarzda bog'lash imkonini beradi.\n\n"

        "Xavfsizlik:\n"
        " - Anonim chatda foydalanuvchilarning ID-lari nazorat qilinadi, bloklangan foydalanuvchilar qayta ulana olmaydi.\n\n"

        "Har qanday savollar yoki yordam uchun /help buyruqni bosing."
    )
    await message.answer(info_text, reply_markup=keyboard.as_markup())
