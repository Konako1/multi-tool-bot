from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


class PollState(StatesGroup):
    start_edit_poll = State()
    edit_poll_question = State()
    edit_poll_option = State()
    add_poll_option = State()
    delete_poll_option = State()


class PollEditText(CallbackData, prefix='text'):
    is_question: bool
    is_option: bool


class PollAddOption(CallbackData, prefix='add_option'):
    pass


class PollDeleteOption(CallbackData, prefix='delete_option'):
    pass


class PollEditAnonymous(CallbackData, prefix='anon'):
    pass


class PollEditMultipleChoice(CallbackData, prefix='multiple'):
    pass


class PollEditFinish(CallbackData, prefix='finish'):
    pass


class PollEditOptionText(CallbackData, prefix='edit_option_text'):
    position: int


async def send_poll_edit_kb(message: Message, state: FSMContext):
    poll_data = await state.get_data()
    button_anonymous_text = 'Disable anonymous voting' \
        if poll_data['is_anonymous'] \
        else 'Enable anonymous voting'

    button_multiple_choice_text = 'Disable multiple choice' \
        if poll_data['is_multiple'] \
        else 'Enable multiple choice'

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Edit question text',
                    callback_data=PollEditText(is_question=True, is_option=False).pack())
            ],
            [
                InlineKeyboardButton(
                    text='Edit option text',
                    callback_data=PollEditText(is_question=False, is_option=True).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=button_anonymous_text,
                    callback_data=PollEditAnonymous().pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=button_multiple_choice_text,
                    callback_data=PollEditMultipleChoice().pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='Finish editing',
                    callback_data=PollEditFinish().pack()
                )
            ]
        ]
    )
    if len(poll_data['options']) > 2:
        kb.inline_keyboard.insert(
            2,
            [
                InlineKeyboardButton(
                    text='Delete option',
                    callback_data=PollDeleteOption().pack()
                )
            ]
        )
    if len(poll_data['options']) < 10:
        kb.inline_keyboard.insert(
            2,
            [
                InlineKeyboardButton(
                    text='Add option',
                    callback_data=PollAddOption().pack()
                )
            ]
        )
    await message.reply('What you want to do with this poll?', reply_markup=kb)
