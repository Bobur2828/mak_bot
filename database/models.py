from typing import Any
from sqlalchemy import BigInteger,String,ForeignKey,Column,Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship,Mapped,mapped_column,DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs,async_sessionmaker,create_async_engine
from config import SQLALCHEMY_URL
from typing import List
engine=create_async_engine(SQLALCHEMY_URL,echo=True)
async_session= async_sessionmaker(engine)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Base(AsyncAttrs,DeclarativeBase):
    pass



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id= Column(Integer,unique=True)
    role = Column(String, nullable=True)
    data = Column(String, server_default=func.now())

    def __repr__(self):
        return self.username
    
class Channels(Base):
    __tablename__ = 'channels'
    
    id = Column(Integer, primary_key=True)
    url = Column(String(50))
    chat_id = Column(String(50))

    def __repr__(self):
        return self.chat_id
    

class Kino(Base):
    __tablename__ = 'kino'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    janr = Column(String(100))
    year = Column(String(100))
    attribute = Column(String(100))
    country = Column(String(100))

    download = Column(Integer)
    language = Column(String(100))
    code = Column(Integer, unique=True)  # code maydoni unikal qilib belgilandi
    file_id = Column(Integer)

    def __repr__(self):
        return self.id
    


