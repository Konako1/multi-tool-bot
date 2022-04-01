from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(commands=['cancel'])
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(
        'Operation cancelled'
    )
