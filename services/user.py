from models.user import User


async def add_user(user_id: int, full_name: str, username: str):

    user = User(
        user_id=user_id,
        full_name=full_name,
        username=username
    )

    await user.save()


async def get_user(user_id: int):
    user = await User.get_or_none(user_id=user_id)
    return user