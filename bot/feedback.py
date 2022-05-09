from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db.psql import get_score

FEEDBACK_BUTTONS = ["продолжить",  "изменить"]


class Feedback(StatesGroup):
    waiting_for_company_name = State()
    waiting_for_company_confirm = State()
    waiting_for_feedback = State()
    waiting_for_feedback_confirm = State()


def register_handlers_feedback(dp: Dispatcher):
    dp.register_message_handler(feedback_start, commands="feedback", state="*")
    dp.register_message_handler(company_name, state=Feedback.waiting_for_company_name)
    dp.register_message_handler(company_confirm, state=Feedback.waiting_for_company_confirm)
    dp.register_message_handler(feedback, state=Feedback.waiting_for_feedback)
    dp.register_message_handler(feedback_confirm, state=Feedback.waiting_for_feedback_confirm)


async def feedback_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Введите название компании/услуги')
    await Feedback.waiting_for_company_name.set()


async def company_name(message: types.Message, state: FSMContext):
    company_name = message.text
    await state.update_data(feedback_company_name=company_name)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*FEEDBACK_BUTTONS)

    await Feedback.next()
    await message.reply(
        f'Вы хотите оставить отзыв для "{company_name}", продолжить?',
        reply_markup=keyboard
    )


async def company_confirm(message: types.Message, state: FSMContext):
    # TODO сделать проверку названия по базе
    if message.text.lower() not in FEEDBACK_BUTTONS:
        await message.answer("Пожалуйста, подтвердите название, используя клавиатуру ниже.")
        return
    if message.text.lower() == "изменить":
        await message.answer(
            'Введите название компании/услуги',
            reply_markup=types.ReplyKeyboardRemove()
        )
        await Feedback.waiting_for_company_name.set()
        return
    user_data = await state.get_data()
    code, msg = await get_score(company_name=user_data['feedback_company_name'])
    if code != 200:
        await message.answer(
            'Данное название компании/услуги не было найдено.'
            'Вы можете попробовать ввести название еще раз,'
            'или оставить отзыв на другую компанию/услугу',
            reply_markup=types.ReplyKeyboardRemove()
        )
        await Feedback.waiting_for_company_name.set()
        return
    await Feedback.next()
    await message.answer(
        f'Пожалуйста, напишите ваш отзыв',
        reply_markup=types.ReplyKeyboardRemove()
    )


async def feedback(message: types.Message, state: FSMContext):
    await state.update_data(feedback=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*FEEDBACK_BUTTONS)

    await Feedback.next()
    await message.reply(
        f'Вы хотите отправить данный отзыв. Продолжить?',
        reply_markup=keyboard
    )


async def feedback_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() not in FEEDBACK_BUTTONS:
        await message.answer("Пожалуйста, подтвердите название, используя клавиатуру ниже.")
        return
    if message.text.lower() == "изменить":
        # TODO выводить отзыв в поле ввода
        await message.answer(
            'Пожалуйста, измените ваш отзыв',
            reply_markup=types.ReplyKeyboardRemove()
        )
        await Feedback.waiting_for_feedback.set()
        return
    user_data = await state.get_data()
    feedback_msg = user_data.get('feedback')
    # TODO передать отзыв в модельку
    feedback_company_name = user_data.get('feedback_company_name')

    await message.answer(
        f'Спасибо, что оставили отзыв для "{feedback_company_name}"! '
        f'Приходите еще!',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()
