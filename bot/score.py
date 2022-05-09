from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db.psql import get_score


class Score(StatesGroup):
    waiting_for_company_name = State()


def register_handlers_score(dp: Dispatcher):
    dp.register_message_handler(score_start, commands="score", state="*")
    dp.register_message_handler(score_print, state=Score.waiting_for_company_name)


async def score_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Введите название компании/услуги')
    await Score.waiting_for_company_name.set()


async def score_print(message: types.Message, state: FSMContext):
    company_name = message.text
    code, answer = await get_score(company_name=company_name)
    if code != 200:
        await message.answer(answer + "\nПопробуйте еще раз")
        return

    await message.answer(f"Оценка компании {company_name}: {answer}")
    await state.finish()
