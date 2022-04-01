from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from .utils import PollEditAnonymous, send_poll_edit_kb

router = Router()


@router.callback_query(PollEditAnonymous.filter())
async def poll_edit_anonymous(query: CallbackQuery, state: FSMContext):
    poll_data = await state.get_data()
    is_anonymous = poll_data['is_anonymous']
    await state.update_data(
        is_anonymous=not is_anonymous
    )

    await send_poll_edit_kb(query.message, state)
