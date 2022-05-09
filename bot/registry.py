from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db.psql import add_company

CONFIRM_BUTTONS = ["подтвердить", "изменить"]


class OrderRegistry(StatesGroup):
    waiting_for_company_name = State()
    waiting_for_confirmation = State()


def register_handlers_registry(dp: Dispatcher):
    dp.register_message_handler(registry_start, commands="registry", state="*")
    dp.register_message_handler(entering_name, state=OrderRegistry.waiting_for_company_name)
    dp.register_message_handler(name_confirmation, state=OrderRegistry.waiting_for_confirmation)


async def registry_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Введите название компании/услуги')
    await OrderRegistry.waiting_for_company_name.set()


async def entering_name(message: types.Message, state: FSMContext):
    await state.update_data(company_name=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*CONFIRM_BUTTONS)

    await OrderRegistry.next()
    await message.reply("Подтвердите введенное название:", reply_markup=keyboard)


async def name_confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() not in CONFIRM_BUTTONS:
        await message.answer("Пожалуйста, подтвердите название, используя клавиатуру ниже.")
        return
    if message.text.lower() == "изменить":
        await message.answer(
            'Введите название компании/услуги',
            reply_markup=types.ReplyKeyboardRemove()
        )
        await OrderRegistry.waiting_for_company_name.set()
        return
    user_data = await state.get_data()
    if user_data['company_name']:
        await add_company(user_data['company_name'])
    await message.answer(f"Компания '{user_data['company_name']}' зарегистрирована.\n"
                         f"Чтобы узнать средний балл вашей компании, воспользуйтесь"
                         f"командой /score", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

