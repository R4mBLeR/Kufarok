from handlers import utils
from dp_init import dp
from aiogram import executor


def start_up():
    print('Bot is started')


utils.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start_up())
