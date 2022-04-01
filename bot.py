import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import TG_TOKEN
from message_handlers import pic_to_sticker_convert_handler, start_handler, poll_editor, cancel_handler


async def main():
    bot = Bot(token=TG_TOKEN, parse_mode='html')
    await bot.set_my_commands([
        BotCommand(command='start', description='Hello'),
        BotCommand(command='make_sticker', description='Converts pic into tg sticker pic format'),
        BotCommand(command='edit_poll', description='Edit poll\'s data'),
    ])
    dp = Dispatcher()
    dp.include_router(pic_to_sticker_convert_handler.router)
    dp.include_router(start_handler.router)
    dp.include_router(poll_editor.router)
    dp.include_router(cancel_handler.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
