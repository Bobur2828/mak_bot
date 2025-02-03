from database.models import User
from database.models import async_session,engine
from sqlalchemy import select,update,delete,desc
from sqlalchemy.orm import Session
from aiogram import  Bot
from sqlalchemy import func
from sqlalchemy import BigInteger,String,ForeignKey,Column,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

bot=Bot
async def get_user():
    query = select(User)
    try:
        async with async_session() as session:
            result = await session.execute(query)
            users = result.scalars().all()
            user_ids = [user.tg_id for user in users if user.tg_id is not None]
            user_count = len(user_ids)
            return user_count
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return 0

async def find_user(tg_id):
    query = select(User)
    try:
        async with async_session() as session:
            result = await session.execute(query.where(User.tg_id == tg_id))
            user = result.scalar_one_or_none()
            return user
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return None
    

async def find_admins():
    query = select(User).where(User.role == "admin")
    try:
        async with async_session() as session:
            result = await session.execute(query)
            admins = result.scalars().all()  # Barcha admin foydalanuvchilarni olish
            admin_ids = [admin.tg_id for admin in admins]  # Barcha adminlarning tg_idlarini ro'yxatga olish
            return admin_ids  # Ro'yxatni qaytarish
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return []



async def update_user(tg_id, new_role):
    query = update(User).where(User.tg_id == tg_id).values(role=new_role).execution_options(synchronize_session="fetch")
    
    try:
        async with async_session() as session:
            # Yangilash so'rovini bajarish
            await session.execute(query)
            await session.commit()  # O'zgarishlarni bazada saqlash
            return True
    except Exception as e:
        print(f"Ma'lumotlar bazasini yangilashda xatolik yuz berdi: {e}")
        return False

    
async def create_user(tg_id: int):
    async with async_session() as session:
        try:
            existing_user = await session.execute(select(User).filter(User.tg_id == tg_id))
            existing_user = existing_user.scalar_one_or_none()
            if existing_user:
                print(f"User with tg_id {tg_id} already exists. Skipping...")
                return  
            new_user = User(tg_id=tg_id)
            session.add(new_user)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def count_users() -> int:
    query = select(func.count(User.id))  # User modelidagi barcha foydalanuvchilarni sanash
    try:
        async with async_session() as session:
            result = await session.execute(query)
            user_count = result.scalar()  # Sanash natijasini olish
            return user_count
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return 0
    

    
async def get_users_tg_ids():
    query = select(User)

    try:
        async with async_session() as session:
            result = await session.execute(query)
            users = result.scalars().all()
            tg_ids = [user.tg_id for user in users if user.tg_id is not None]
            return tg_ids
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return []