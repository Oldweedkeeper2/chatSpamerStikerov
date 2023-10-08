from typing import Union, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from data.engine import get_database
from data.models import StickerSchedule, Chat, Sticker


class StickerScheduleRepository:
    @staticmethod
    async def add_schedule(chat_id: int, sticker_file_id: str) -> Union[StickerSchedule, None]:
        async with get_database() as connect:  # type: AsyncSession
            try:
                # Находим существующий чат и стикер по chat_id и sticker_file_id
                chat_result = await connect.execute(select(Chat).where(Chat.chat_id == chat_id))
                chat = chat_result.scalar_one_or_none()
                
                sticker_result = await connect.execute(select(Sticker).where(Sticker.file_id == sticker_file_id))
                sticker = sticker_result.scalar_one_or_none()
                
                if chat and sticker:
                    # Если оба найдены, создаем новую запись в StickerSchedule
                    new_schedule = StickerSchedule(chats_id=chat.id, stickers_id=sticker.id)
                    connect.add(new_schedule)
                    await connect.commit()
                    await connect.refresh(new_schedule)
                    return new_schedule
                else:
                    print(f"Chat or Sticker not found: Chat - {chat}, Sticker - {sticker}")
                    return None
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return None
    
    @staticmethod
    async def get_schedule(id: int) -> Union[StickerSchedule, None]:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(select(StickerSchedule).where(StickerSchedule.id == id))
                schedule = result.scalar_one_or_none()
                return schedule
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
    
    @staticmethod
    async def get_all_schedule() -> List[StickerSchedule]:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(
                        select(StickerSchedule)
                        .options(
                                selectinload(StickerSchedule.chat),
                                selectinload(StickerSchedule.sticker)
                        )
                )
                schedule = result.scalars().all()
                return schedule
            except Exception as e:
                print(f"An error occurred: {e}")
                return []
    
    @staticmethod
    async def update_schedule(id: int, chats_id: int, stickers_id: int) -> bool:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(select(StickerSchedule).where(StickerSchedule.id == id))
                schedule = result.scalar_one_or_none()
                if schedule:
                    schedule.chats_id = chats_id
                    schedule.stickers_id = stickers_id
                    await connect.commit()
                    return True
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return False
    
    @staticmethod
    async def delete_schedule(id: int) -> bool:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(select(StickerSchedule).where(StickerSchedule.id == id))
                schedule = result.scalar_one_or_none()
                if schedule:
                    await connect.delete(schedule)
                    await connect.commit()
                    return True
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return False
