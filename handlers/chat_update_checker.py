import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import ChatMemberUpdatedFilter, PROMOTED_TRANSITION, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated

from data.methods.chat_methods import ChatRepository
from data.methods.sticker_methods import StickerRepository

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(PROMOTED_TRANSITION))
async def entering_the_channel(chat_member: ChatMemberUpdated, bot: Bot):
    await asyncio.sleep(1)  # Пауза для убеждения, что сообщение отправлено
    chat_id = int(chat_member.chat.id)
    bot_status = str(chat_member.new_chat_member.status)
    name = str(chat_member.chat.full_name)
    await ChatRepository.add_chat(chat_id=chat_id,
                                  name=name,
                                  bot_status=bot_status)


@router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def my_chat_member_change(chat_member: ChatMemberUpdated, bot: Bot) -> None:
    chat_id = chat_member.chat.id
    old_chat_member = chat_member.old_chat_member
    new_chat_member = chat_member.new_chat_member
    # удаляем чат из бд.
    await ChatRepository.delete_chat(chat_id=chat_id)
