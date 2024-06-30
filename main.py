import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import logging

API_TOKEN = '6316836463:AAHwIinZ9H9aOS85sDO2RnXmcGdrfS2GGIA'

# Logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
Bot.set_current(bot)  # Set the bot instance
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Group usernames list
group_usernames = ["@romitanim"]  # o'zingizning guruh usernameslarini qo'shing

# Group IDs list
group_ids = []

# Postni saqlash uchun o'zgaruvchi
latest_post = None

# Admin ID
ADMIN_ID = 5875465209  # faqat sizning ID bo'lishi kerak

# /start va /help buyruqlari
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Bu bot siz tashlagan postlarni har 30 daqiqada guruhlarga yuboradi.")

# Post qabul qilish
@dp.message_handler(content_types=types.ContentType.ANY)
async def receive_post(message: types.Message):
    global latest_post
    if message.from_user.id == ADMIN_ID:
        latest_post = message
        await message.reply("Post qabul qilindi!")
    else:
        await message.reply("Sizda bu buyruqni bajarish huquqi yo'q.")

# Har 30 daqiqada postlarni guruhlarga yuborish
async def periodic_post():
    while True:
        if latest_post:
            for group_id in group_ids:
                try:
                    await latest_post.copy_to(group_id)
                except Exception as e:
                    logging.error(f"Failed to send post to group {group_id}: {e}")
        await asyncio.sleep(5)  # 30 daqiqa

# Username dan chat_id olish
async def get_chat_ids():
    global group_ids
    for username in group_usernames:
        try:
            chat = await bot.get_chat(username)
            group_ids.append(chat.id)
        except Exception as e:
            logging.error(f"Failed to get chat ID for {username}: {e}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_chat_ids())  # Initial chat IDs fetching
    loop.create_task(periodic_post())
    executor.start_polling(dp, skip_updates=True)
