from aiogram.filters.state import StatesGroup, State


class ScheduleState(StatesGroup):
    chat_id = State()
