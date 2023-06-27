from handlers import client
from dp_init import dp
from aiogram import executor


def start_up():
    print('[LOG:] Bot is started')


client.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start_up())
