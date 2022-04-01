from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from .utils import send_poll_edit_kb, PollEditMultipleChoice

router = Router()


@router.callback_query(PollEditMultipleChoice.filter())
async def poll_edit_multiple(query: CallbackQuery, state: FSMContext):
    poll_data = await state.get_data()
    is_multiple = poll_data['is_multiple']
    await state.update_data(
        is_multiple=not is_multiple
    )

    await send_poll_edit_kb(query.message, state)
