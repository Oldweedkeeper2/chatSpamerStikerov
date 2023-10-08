from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from data.models import Sticker
from data.engine import get_database
from typing import Union, List


class StickerRepository:
    
    @staticmethod
    async def add_sticker(file_id: str) -> Union[Sticker, None]:
        async with get_database() as connect:  # type: AsyncSession
            try:
                new_sticker = Sticker(file_id=file_id)
                connect.add(new_sticker)
                await connect.commit()
                await connect.refresh(new_sticker)
                return new_sticker
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return None
    
    @staticmethod
    async def get_sticker(sticker_id: int) -> Union[Sticker, None]:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(select(Sticker).where(Sticker.id == sticker_id))
                sticker = result.scalar_one_or_none()
                return sticker
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
    
    @staticmethod
    async def update_sticker(sticker_id: int, file_id: str) -> bool:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(select(Sticker).where(Sticker.id == sticker_id))
                sticker = result.scalar_one_or_none()
                if sticker:
                    sticker.file_id = file_id
                    await connect.commit()
                    return True
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return False
    
    @staticmethod
    async def delete_sticker(sticker_id: int) -> bool:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(select(Sticker).where(Sticker.id == sticker_id))
                sticker = result.scalar_one_or_none()
                if sticker:
                    await connect.delete(sticker)
                    await connect.commit()
                    return True
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return False
