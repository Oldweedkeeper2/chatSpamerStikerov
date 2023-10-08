# # f_inline_bot
# from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated, BotKicked
#
# import logging
#
# logging.basicConfig(level=logging.INFO)
#
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils import executor
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from datetime import datetime, timedelta
# import logging
# import re
#
# logging.basicConfig(level=logging.INFO)
# API_TOKEN = '6493978630:AAG2XOj9hKGgAQCvpn-y4RXf5NK8YbpKUk0'
#
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
#
# # Формат: {chat_id: {'sticker': sticker_id, 'times': [(time1, auto_renew1), (time2, auto_renew2), ...], 'active': True}}
# sticker_storage = {}
#
#
# async def send_sticker():
#     current_time = datetime.now().strftime('%H:%M')
#     for chat_id, data in sticker_storage.items():
#         sticker_id = data.get('sticker')
#         times = data.get('times', [])
#
#         for time, auto_renew in times:
#             if current_time == time:
#                 try:
#                     await bot.send_sticker(chat_id, sticker_id)
#                     if not auto_renew:
#                         times.remove((time, auto_renew))
#                 except Exception as e:
#                     logging.error(f"Failed to send sticker to chat {chat_id}: {e}")
#
#
# @dp.message_handler(chat_type="private", commands=['start'])
# async def handle_start(message: types.Message):
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("Заменить стикер", callback_data="replace_sticker"))
#     await message.reply("Нажмите на кнопку, чтобы заменить стикер.", reply_markup=markup)
#
#
# temp_chat_id_storage = {}
#
#
# @dp.callback_query_handler(lambda c: c.data == 'replace_sticker')
# async def handle_replace_sticker(callback_query: types.CallbackQuery):
#     await bot.send_message(callback_query.from_user.id, "Введите ID чата, для которого хотите заменить стикер.")
#
#
# @dp.message_handler(chat_type="private", content_types=['text'])
# async def handle_chat_id_input(message: types.Message):
#     chat_id = message.text
#     if re.match(r'-?\d+', chat_id):
#         temp_chat_id_storage[message.from_user.id] = chat_id
#         await message.reply("Отправьте новый стикер.")
#     else:
#         await message.reply("Введите корректный ID чата.")
#
#
# @dp.message_handler(chat_type="private", content_types=['sticker'])
# async def handle_private_sticker(message: types.Message):
#     user_id = message.from_user.id
#     chat_id = temp_chat_id_storage.get(user_id)
#
#     if chat_id:
#         if chat_id not in sticker_storage:
#             sticker_storage[chat_id] = {'sticker': None, 'times': []}
#         sticker_storage[chat_id]['sticker'] = message.sticker.file_id
#         await message.reply(f"Стикер заменён для чата с ID {chat_id}. Теперь введите время в формате HH:MM.")
#         del temp_chat_id_storage[user_id]
#
#
# @dp.message_handler(chat_type="private", content_types=['text'])
# async def handle_time_input(message: types.Message):
#     time = message.text
#     if re.match(r'\d{2}:\d{2}', time):
#         chat_id = temp_chat_id_storage.get(message.from_user.id)
#         if chat_id:
#             sticker_storage[chat_id]['times'].append((time, True))
#             await message.reply(f"Время {time} добавлено для чата с ID {chat_id}.")
#         else:
#             await message.reply("Сначала введите ID чата.")
#     else:
#         await message.reply("Введите корректное время.")
#
#
# if __name__ == '__main__':
#     scheduler = AsyncIOScheduler()
#     scheduler.add_job(send_sticker, 'interval', minutes=1)
#     scheduler.start()
#
#     executor.start_polling(dp, skip_updates=True)
#
