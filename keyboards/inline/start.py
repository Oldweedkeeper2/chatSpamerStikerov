from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Посмотреть текущие рассылки", callback_data="current_newsletters"),
            # тут будут ещё внутри текущих рассылок дополнительные кнопки по выбору чата и установки рассылки,
            # а также ограничение до 10 рассылок на человека
            InlineKeyboardButton(text="Добавить рассылку", callback_data="create_newsletters")
        ],
        [
            InlineKeyboardButton(text="Подтвердить", callback_data="accept")  # это не нужно, просто показал пример того
            # как формируются кнопки в aiogram 3
        ],
        [
        
        ]
    ]
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard_markup
