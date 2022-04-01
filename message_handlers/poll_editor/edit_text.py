from aiogram import Router, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from .utils import PollEditText, PollState
from .utils import PollEditOptionText, send_poll_edit_kb

router = Router()


@router.callback_query(PollEditText.filter(F.is_question))
async def poll_edit_question_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(PollState.edit_poll_question)
    await query.message.reply(
        'Write new poll question'
    )


@router.message(PollState.edit_poll_question)
async def poll_edit_question(message: Message, state: FSMContext):
    await state.set_state(PollState.start_edit_poll)
    await state.update_data(
        question=message.text,
    )

    await send_poll_edit_kb(message, state)


@router.callback_query(PollEditText.filter(F.is_option))
async def poll_choose_option_to_edit(query: CallbackQuery, state: FSMContext):
    await state.set_state(PollState.edit_poll_option)
    poll_data = await state.get_data()
    poll_options: list[str] = poll_data['options']
    inline_kb_buttons: list[list[InlineKeyboardButton]] = []
    for i, option_text in enumerate(poll_options):
        inline_kb_buttons.append(
            [
                InlineKeyboardButton(
                    text=option_text,
                    callback_data=PollEditOptionText(position=i).pack()
                )
            ]
        )

    kb = InlineKeyboardMarkup(
        inline_keyboard=inline_kb_buttons,
    )

    await query.message.reply(
        'Pick option to edit',
        reply_markup=kb,
    )


@router.callback_query(PollEditOptionText.filter(), PollState.edit_poll_option)
async def poll_edit_option_handler(query: CallbackQuery, state: FSMContext, callback_data: PollEditOptionText):
    await state.update_data(
        position=callback_data.position
    )
    await query.message.reply(
        'Write new option text'
    )


@router.message(PollState.edit_poll_option)
async def poll_edit_option(message: Message, state: FSMContext):
    await state.set_state(PollState.start_edit_poll)
    poll_data = await state.get_data()
    poll_options: list[str] = poll_data['options']
    poll_options[poll_data['position']] = message.text

    await state.update_data(
        options=poll_options,
    )

    await send_poll_edit_kb(message, state)
