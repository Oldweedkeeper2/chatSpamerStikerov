from typing import Any

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.handlers import MessageHandler
from aiogram.methods import SendMessage
from aiogram.types import Message

router = Router()


@router.message()
async def handle(message: Message, state: FSMContext) -> Any:
    await message.answer('Это бот для рассылок, введи /start, чтобы начать работу!')
