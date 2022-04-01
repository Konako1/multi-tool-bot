from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from .utils import PollState, PollEditFinish, send_poll_edit_kb

router = Router()


@router.message(commands=['edit_poll'])
async def edit_poll_handler(message: Message, state: FSMContext):
    await state.set_state(PollState.start_edit_poll)
    await message.reply(
        'Send me poll to edit.'
    )


@router.message(content_types=['poll'])
async def edit_poll_options(message: Message, state: FSMContext):
    await state.update_data(
        question=message.poll.question,
        options=[option.text for option in message.poll.options],
        is_anonymous=message.poll.is_anonymous,
        is_multiple=message.poll.allows_multiple_answers
    )

    await send_poll_edit_kb(message, state)


@router.message(PollState.start_edit_poll)
async def edit_poll_wrong_content_type(message: Message):
    await message.reply(
        'Send me poll, not something else.'
    )


@router.callback_query(PollEditFinish.filter())
async def poll_edit_finish(query: CallbackQuery, state: FSMContext):
    poll_data = await state.get_data()
    await query.message.reply_poll(
        question=poll_data['question'],
        options=poll_data['options'],
        is_anonymous=poll_data['is_anonymous'],
        allows_multiple_answers=poll_data['is_multiple']
    )
    await state.clear()
