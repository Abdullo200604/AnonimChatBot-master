from aiogram import Dispatcher
from handlers import start, plans, random_func, encryption, anonim


def register_all_handlers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(random_func.router)
    dp.include_router(encryption.router)
    dp.include_router(anonim.router)
    dp.include_router(plans.router)
