from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String, Boolean, Integer, TIMESTAMP, ForeignKey, Column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, Mapped

from config import *
from models.models import role

# в качестве адаптера базы данных используем sqlalchemy

# asyncpg - драйвер для асинхронной работы с базой данных
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# метаданные
Base: DeclarativeMeta = declarative_base()


# класс пользователя
class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


# точка входа sqlalchemy в наше приложение
engine = create_async_engine(DATABASE_URL)
# с помощью этого движка создаём сессии(временнные соеденения), чтобы можно было работать с бд
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# получение ассинхронной сессии через контексный менеджер
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
