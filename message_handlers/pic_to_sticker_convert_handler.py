from io import BytesIO

from PIL import Image
from aiogram import Bot, Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, BufferedInputFile


class Form(StatesGroup):
    pic_to_sticker = State()


router = Router()


def convert_photo(file: BytesIO):
    file.seek(0)
    sticker: Image.Image = Image.open(file)
    sticker.thumbnail((512, 512))
    file.seek(0)
    sticker.save(file, 'png')
    file.seek(0)


@router.message(commands=['make_sticker'])
async def pic_to_sticker_convert_handler(message: Message, state: FSMContext):
    await state.set_state(Form.pic_to_sticker)
    await message.reply(
        'Send me picture to convert into sticker'
    )


@router.message(Form.pic_to_sticker, content_types=['photo'])
async def pic_to_sticker_converter(message: Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    file = BytesIO()
    await bot.download(photo, file)
    convert_photo(file)
    await bot.send_chat_action(message.chat.id, 'upload_photo')
    await message.reply_document(BufferedInputFile(file.read(), 'file.png'))
    await state.clear()


@router.message(Form.pic_to_sticker)
async def pic_to_sticker_wrong_content_type(message: Message):
    await message.reply(
        'Send me photo, not something else'
    )
