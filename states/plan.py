from aiogram.fsm.state import State, StatesGroup

class PlanAdd(StatesGroup):
    plan_text = State()
    plan_time = State()
    finish = State()