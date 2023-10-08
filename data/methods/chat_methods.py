from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from data.models import Chat
from data.engine import get_database
from typing import Union, List


class ChatRepository:
    @staticmethod
    async def add_chat(chat_id: int, bot_status: str, name: str) -> Union[Chat, None]:
        async with get_database() as connect:  # type: AsyncSession
            try:
                new_chat = Chat(name=name,
                                chat_id=chat_id,
                                bot_status=bot_status)
                connect.add(new_chat)
                await connect.commit()
                await connect.refresh(new_chat)
                return new_chat
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return None
    
    @staticmethod
    async def get_chat(chat_id: int) -> Union[Chat, None]:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(select(Chat).where(Chat.chat_id == chat_id))  # Note: use Chat.chat_id, not Chat.id
                chat = result.scalar_one_or_none()
                return chat
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

    
    @staticmethod
    async def update_chat_name(chat_id: int, name: str) -> bool:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(select(Chat).where(Chat.id == chat_id))
                chat = result.scalar_one_or_none()
                if chat:
                    chat.name = name
                    await connect.commit()
                    return True
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return False
    
    @staticmethod
    async def delete_chat(chat_id: int) -> bool:
        async with get_database() as connect:  # type: AsyncSession
            try:
                result = await connect.execute(select(Chat).where(Chat.chat_id == chat_id))
                chat = result.scalar_one_or_none()
                if chat:
                    await connect.delete(chat)
                    await connect.commit()
                    return True
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return False
    
    @staticmethod
    async def update_chat_status(chat_id: int, status: str) -> bool:
        async with get_database() as connect:  # type: AsyncSession
            try:
                chat = await connect.execute(select(Chat).where(Chat.id == chat_id))
                chat = chat.scalar_one()
                if chat:
                    chat.bot_status = status
                    await connect.commit()
                    return True
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                await connect.rollback()
                return False
    
    @staticmethod
    async def is_chat_registered(chat_id: int) -> Union[bool, None]:
        try:
            async with get_database() as connect:  # type: AsyncSession
                chat = await connect.execute(select(Chat).where(Chat.id == chat_id))
                return chat.scalar_one_or_none() is not None
        except Exception as e:
            print(f"An error occurred: {e}")
            await connect.rollback()
            return False
