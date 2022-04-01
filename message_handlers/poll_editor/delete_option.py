from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from message_handlers.poll_editor.utils import PollDeleteOption, PollState, PollEditOptionText, send_poll_edit_kb

router = Router()


@router.callback_query(PollDeleteOption.filter())
async def poll_choose_option_to_delete(query: CallbackQuery, state: FSMContext):
    await state.set_state(PollState.delete_poll_option)
    poll_data = await state.get_data()
    poll_options: list[str] = poll_data['options']
    inline_kb_buttons: list[list[InlineKeyboardButton]] = []
    for i, option_text in enumerate(poll_options):
        inline_kb_buttons.append(
            [
                InlineKeyboardButton(
                    text=f"Delete «{option_text}»",
                    callback_data=PollEditOptionText(position=i).pack()
                )
            ]
        )

    kb = InlineKeyboardMarkup(
        inline_keyboard=inline_kb_buttons,
    )

    await query.message.reply(
        text='Pick option to delete',
        reply_markup=kb,
    )


@router.callback_query(PollEditOptionText.filter(), PollState.delete_poll_option)
async def poll_delete_option(query: CallbackQuery, state: FSMContext, callback_data: PollEditOptionText):
    await state.set_state(PollState.start_edit_poll)
    poll_data = await state.get_data()
    poll_options: list[str] = poll_data['options']
    poll_options.pop(callback_data.position)

    await state.update_data(
        options=poll_options,
    )

    await send_poll_edit_kb(query.message, state)
