from database.models import Channels
from database.models import async_session,engine
from sqlalchemy import select,update,delete,desc
from sqlalchemy.orm import Session
from aiogram import  Bot
from sqlalchemy import func
from sqlalchemy import BigInteger,String,ForeignKey,Column,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from database.requests import users

bot=Bot
async def get_channel_urls() -> list:
    query = select(Channels.url)
    try:
        async with async_session() as session:
            result = await session.execute(query)
            urls = result.scalars().all()  # `url` ro'yxatini olish
            return urls
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        # return []
    
async def get_channel_chat_ids() -> list:
    query = select(Channels.chat_id)
    try:
        async with async_session() as session:
            result = await session.execute(query)
            chat_ids = result.scalars().all()  # `chat_id` ro'yxatini olish
            return chat_ids
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return []
    
async def get_channel_url_by_chat_id(chat_id: str) -> str:
    query = select(Channels.url).where(Channels.chat_id == chat_id)
    try:
        async with async_session() as session:
            result = await session.execute(query)
            url = result.scalar_one_or_none()  # Birgina URL ni olish
            return url
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return None
    

async def create_channel(chat_id: int,url: str):
    async with async_session() as session:
        try:
            existing_user = await session.execute(select(Channels).filter(Channels.chat_id == chat_id))
            existing_user = existing_user.scalar_one_or_none()
            if existing_user:
                print(f"User with tg_id {chat_id} already exists. Skipping...")
                return  
            new_user = Channels(chat_id=chat_id,url=url)
            session.add(new_user)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()



async def delete_channel(chat_id: int):
    async with async_session() as session:
        try:
            # Kanalni topish
            result = await session.execute(select(Channels).filter(Channels.chat_id == chat_id))
            existing_channel = result.scalar_one_or_none()
            
            if existing_channel:
                # Kanalni o'chirish
                await session.delete(existing_channel)
                await session.commit()
                print(f"Channel with chat_id {chat_id} deleted successfully.")
            else:
                print(f"No channel found with chat_id {chat_id}.")
        
        except Exception as e:
            await session.rollback()
            print(f"An error occurred: {e}")
            raise e

async def get_channels() -> list:
    query = select(Channels)
    try:
        async with async_session() as session:
            result = await session.execute(query)
            chat_ids = result.scalars().all()  # `chat_id` ro'yxatini olish
            return chat_ids
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return []