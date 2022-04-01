from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from .utils import PollAddOption, PollState, send_poll_edit_kb, PollEditOptionText

router = Router()


@router.callback_query(PollAddOption.filter())
async def poll_choose_option_to_add(query: CallbackQuery, state: FSMContext):
    await state.set_state(PollState.add_poll_option)
    poll_data = await state.get_data()
    poll_options: list[str] = poll_data['options']
    inline_kb_buttons: list[list[InlineKeyboardButton]] = []
    for i, option_text in enumerate(poll_options):
        inline_kb_buttons.append(
            [
                InlineKeyboardButton(
                    text=f"Add before «{option_text}»",
                    callback_data=PollEditOptionText(position=i).pack()
                )
            ]
        )

    inline_kb_buttons.append([
        InlineKeyboardButton(
            text=f"Add last",
            callback_data=PollEditOptionText(position=len(poll_options)).pack()
        )
    ])

    kb = InlineKeyboardMarkup(
        inline_keyboard=inline_kb_buttons,
    )

    await query.message.reply(
        text='Pick position of the new option',
        reply_markup=kb,
    )


@router.callback_query(PollEditOptionText.filter(), PollState.add_poll_option)
async def poll_add_option_handler(query: CallbackQuery, state: FSMContext, callback_data: PollEditOptionText):
    await state.update_data(
        position=callback_data.position
    )
    await query.message.reply(
        'Write new option text'
    )


@router.message(PollState.add_poll_option)
async def poll_add_option(message: Message, state: FSMContext):
    await state.set_state(PollState.start_edit_poll)
    poll_data = await state.get_data()
    poll_options: list[str] = poll_data['options']
    poll_options.insert(poll_data['position'], message.text)

    await state.update_data(
        options=poll_options,
    )

    await send_poll_edit_kb(message, state)
