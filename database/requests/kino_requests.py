import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import async_session,engine
from sqlalchemy import func
from database.models import Kino
async def generate_unique_code(session: AsyncSession) -> int:
    """4 xonali unique code generatsiya qiladi"""
    while True:
        # 4 xonali random son generatsiya qilish
        new_code = random.randint(1000, 9999)
        
        # Kodning unikal ekanligini tekshirish
        result = await session.execute(select(Kino).filter_by(code=new_code))
        existing_code = result.scalar_one_or_none()
        
        if not existing_code:
            return new_code

async def create_kino(title: str,attribute:str ,janr: str, year: str, country: str, download: int, language: str, file_id: int):
    async with async_session() as session:
        try:
            # Unikal code generatsiya qilish
            code = await generate_unique_code(session)
            
            # Kino yozuvini yaratish
            new_kino = Kino(
                title=title,
                janr=janr,
                attribute=attribute,
                year=year,
                country=country,
                download=download,
                language=language,
                file_id=file_id,
                code=code  # generatsiya qilingan kodni qo'shish
            )
            
            session.add(new_kino)
            await session.commit()
            return new_kino
        except Exception as e:
            await session.rollback()
            print(f"Kino yozuvini yaratishda xatolik yuz berdi: {e}")
            raise
        finally:
            await session.close()



async def find_kino(title):
    query = select(Kino)
    try:
        async with async_session() as session:
            result = await session.execute(query.where(Kino.title == title))
            user = result.scalar_one_or_none()
            return user
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return None
from sqlalchemy.exc import SQLAlchemyError   
async def find_kino_code(code):
    query = select(Kino).where(Kino.code == code)
    try:
        async with async_session() as session:
            result = await session.execute(query)
            kino = result.scalar_one_or_none()

            if kino:
                # Increment the download count
                kino.download += 1
                # Commit the transaction to save changes
                await session.commit()

                # Refetch in a new session if necessary
                async with async_session() as new_session:
                    refetched_result = await new_session.execute(query)
                    kino = refetched_result.scalar_one_or_none()

                return kino
    except SQLAlchemyError as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return None
    
async def delete_kino_by_id(kino_id: int):
    async with async_session() as session:  # Use your session creation method here
        try:
            # Query to find the Kino record by its ID
            query = select(Kino).where(Kino.id == kino_id)
            result = await session.execute(query)
            kino = result.scalar_one_or_none()
            
            if kino:
                # Delete the Kino record if it exists
                await session.delete(kino)
                await session.commit()
                print(f"Kino record with ID {kino_id} has been deleted.")
                return True
            else:
                print(f"Kino record with ID {kino_id} not found.")
                return False

        except Exception as e:
            print(f"An error occurred while deleting the Kino record: {e}")
            await session.rollback()
            return False


async def get_kinos() -> list:
    query = select(Kino)
    try:
        async with async_session() as session:
            result = await session.execute(query)
            chat_ids = result.scalars().all()  # `chat_id` ro'yxatini olish
            return chat_ids
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return []  
    
async def get_random_kino() -> Kino:
    query = select(Kino).order_by(func.random()).limit(1)  # Tasodifiy tartibda bitta kino olish
    try:
        async with async_session() as session:
            result = await session.execute(query)
            kino = result.scalar_one_or_none()  # Yagona kino qaytarish
            await find_kino_code(kino.code)
            return kino
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return None
    
async def get_top_10_kinos() -> list:
    query = select(Kino).order_by(Kino.download.desc()).limit(10)  # Eng katta 'download' qiymatiga ega bo'lgan 10 ta kino olish
    try:
        async with async_session() as session:
            result = await session.execute(query)
            kinos = result.scalars().all()  # Barcha top-10 kinolarni olish
            return kinos
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return []