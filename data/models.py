# base_and_models.py

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import registry
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from data.config import ALCHEMY_DATABASE_URL
from data.engine import engine

mapper_registry = registry()
Base = mapper_registry.generate_base()

# Модель Chat
from sqlalchemy.orm import relationship


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(BigInteger, index=True)
    name = Column(String)
    bot_status = Column(String, nullable=False, default='member')
    schedules = relationship('StickerSchedule', back_populates='chat', cascade="all, delete-orphan")  # Add this line


# Модель Sticker
class Sticker(Base):
    __tablename__ = "stickers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_id = Column(String)
    schedules = relationship('StickerSchedule', back_populates='sticker', cascade="all, delete-orphan")  # Обновите эту строку


class StickerSchedule(Base):
    __tablename__ = 'sticker_schedule'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chats_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    stickers_id = Column(Integer, ForeignKey('stickers.id'), nullable=False)
    # time_to_send = Column(DateTime, nullable=False)
    chat = relationship('Chat', back_populates='schedules')  # Add this line
    sticker = relationship('Sticker', back_populates='schedules')  # Add this line


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # DEBUG MODE
        await conn.run_sync(Base.metadata.create_all)


async def main():
    try:
        await init_models()
        print('Tables created')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
    # asyncio.run(main2())
