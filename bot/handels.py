from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN

from bot.registry import register_handlers_registry
from bot.feedback import register_handlers_feedback
from bot.score import register_handlers_score

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def init_handlers():
    register_handlers_common(dp=dp)
    register_handlers_registry(dp=dp)
    register_handlers_feedback(dp=dp)
    register_handlers_score(dp=dp)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_start, commands="help", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")


async def cmd_start(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(f'Я бот. Приятно познакомиться, {msg.from_user.first_name}')


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
