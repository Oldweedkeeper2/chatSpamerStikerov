from aiogram import Router, F, Bot

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hitalic

from data.methods.chat_methods import ChatRepository
from data.methods.sticker_methods import StickerRepository
from data.methods.sticker_schedule_methods import StickerScheduleRepository
from keyboards.inline.start import get_start_keyboard
from states.shedule import ScheduleState
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()


@router.message(F.chat.type == 'private', Command(commands='start'))
async def handle(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    start_kb = get_start_keyboard()
    await state.clear()
    await message.answer(text='Пожалуйста, отправьте мне стикер.')


@router.message(F.content_type == 'sticker')
async def handle(message: Message, state: FSMContext) -> None:
    sticker_file_id = message.sticker.file_id
    await state.update_data(sticker_file_id=sticker_file_id)
    await message.answer("Стикер сохранен. Теперь пожалуйста введите чат, в котором хотите сделать рассылку")
    await state.set_state(ScheduleState.chat_id)


@router.message(F.content_type == 'text', ScheduleState.chat_id)
async def handle(message: Message, state: FSMContext) -> None:
    try:
        chat_id = int(message.text)
    except ValueError:
        await message.delete()
        await state.set_state(ScheduleState.chat_id)
        return
    data = await state.get_data()
    sticker_file_id = data['sticker_file_id']
    print(sticker_file_id)
    if await ChatRepository.get_chat(chat_id=int(chat_id)):
        await StickerRepository.add_sticker(file_id=sticker_file_id)
        result = await StickerScheduleRepository.add_schedule(chat_id=int(chat_id),
                                                              sticker_file_id=sticker_file_id)
        if result:
            text = "Стикер сохранен. Он будет отправлен в этот чат каждый день в 8 утра."
        else:
            text = f"Видимо бот ещё не добавлен в ваш чат, либо не имеет прав администратора!\n" \
                   f"Попробуйте добавить бота в чат с правами админа и повторить установку рассылки!\n\n" \
                   f"{hitalic('В случае проблем обращайтесь к @Oldweedkeeper')}"
    
    else:
        text = f"Видимо бот ещё не добавлен в ваш чат, либо не имеет прав администратора!\n" \
               f"Попробуйте добавить бота в чат с правами админа и повторить установку рассылки!\n\n" \
               f"{hitalic('В случае проблем обращайтесь к @Oldweedkeeper')}"
    await message.answer(text=text)


async def sched(bot: Bot):
    scheduler_list = await StickerScheduleRepository.get_all_schedule()
    for schedule_item in scheduler_list:
        chat_id = schedule_item.chat.chat_id
        sticker_file_id = schedule_item.sticker.file_id
        try:
            await bot.send_sticker(chat_id=chat_id,
                                   sticker=sticker_file_id)
        except Exception as e:
            print(e)
