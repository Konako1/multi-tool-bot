from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(commands=['start'])
async def start(message: Message):
    await message.reply(
        "Hello, I'm useless."
    )
