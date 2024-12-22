from models.plan import Plan


async def add_plan(user_id: int, plan_time: str, plan_text: str):
    plan = Plan(
        user_id=user_id,
        plan_time=plan_time,
        plan_text=plan_text
    )

    await plan.save()


async def get_plan(user_id: int):
    plan = Plan.get_or_none(user_id=user_id)
    return plan