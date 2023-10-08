from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session
from sqlalchemy.orm import sessionmaker

from data.config import ALCHEMY_DATABASE_URL

engine = create_async_engine(
        ALCHEMY_DATABASE_URL,
        # echo=True,  # DEBUG  # включает логирование SQL-запросов (для отладки).
        pool_size=10,  # Минимальное количество соединений в пуле
        max_overflow=30  # Максимальное количество соединений в пуле
)

AsyncSessionLocal = sessionmaker(bind=engine,  # привязываем движок
                                 expire_on_commit=False,  # объекты не истекают после коммита транзакции.
                                 class_=AsyncSession,  # указываем, что сессии должны быть асинхронными.
                                 autoflush=False,  # указываем, что сессии должны быть асинхронными.
                                 )


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session(AsyncSessionLocal) as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            print(f"Error: {e}")


@asynccontextmanager
async def get_database() -> AsyncGenerator[AsyncSession, None]:
    database: AsyncSession = AsyncSessionLocal()
    try:
        yield database
    except Exception as e:
        await database.rollback()
        print(f"Error: {e}")
    finally:
        await database.close()
