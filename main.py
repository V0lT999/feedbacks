import asyncio
import logging

from aiogram.types.bot_command import BotCommand

from bot.handels import (
    bot,
    dp,
    init_handlers
)


logger = logging.getLogger(__name__)


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Начать работу"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/registry", description="Зарегистрировать компанию/услугу"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    init_handlers()

    await set_commands(bot)

    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
