from database.requests import users

async def is_admin(user_id: int) -> bool:
    admin_ids = await users.find_admins()  # Adminlarning tg_id larini olish
    return user_id in admin_ids