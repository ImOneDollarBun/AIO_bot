import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

bot = Bot('7912991511:AAFEzzrqEYGxG_PB-mcVkQl1_GyX3gibNho', default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

user_messages = {}
ADMIN_ID = '967075635'  # Укажите ID администратора


@dp.message(Command('start'))
async def start(msg: Message):
    await msg.answer("Да, меня написали ради теста. Но ты все еще можешь спросить у админа суперважную инфу.")


@dp.message(F.text == '/ask')
async def ask(msg: Message):
    if msg.from_user.id not in user_messages:
        user_messages[msg.from_user.id] = []  # Инициализация очереди для пользователя

    user_messages[msg.from_user.id].append(msg.text)  # Добавляем сообщение в очередь
    await bot.send_message(ADMIN_ID,
                           f"Новое сообщение от {msg.from_user.full_name} ({msg.from_user.id}):\n{msg.text}")


@dp.message()
async def admin_answ(msg: Message):
    if str(msg.from_user.id) == ADMIN_ID:  # Проверка, что сообщение от администратора
        for user_id, messages in list(user_messages.items()):
            if messages:
                user_message = messages.pop(0)  # Извлекаем первое сообщение из очереди
                await bot.send_message(user_id, f"Ответ от администратора: {msg.text}\n\nНа ваше сообщение:\n{user_message}")
                if not messages:
                    del user_messages[user_id]  # Удаляем пользователя, если больше нет сообщений


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
