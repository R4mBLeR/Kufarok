from dp_init import dp
from handlers import utils
from aiogram import types, Dispatcher


TIMEOUT = 30
search_dict = {}


async def start_command(message: types.message):

    await message.answer('Привет, я написан радиком, для начала моей работы напиши команду /search и укажи что хочешь искать. Пример: /search Мозги радика\nДля остановки поиска воспользуйся /stop\n Бот показывает лишь новые поступающие предложения')


async def search_command(message: types.message):
    try:
        search_dict[message.from_id].close()
        search_dict.pop(message.from_id)
    except:
        pass
    if (message.text == '/search'):
        await message.answer('Вы не написали тему для поиска')
    else:
        search_dict[message.from_id] = utils.checking(message)
        await search_dict[message.from_id]


async def stop_command(message: types.message):
    try:
        search_dict[message.from_id].close()
        search_dict.pop(message.from_id)
        await message.answer('Поиск остановлен')
    except KeyError:
        await message.answer('Вы ничего не искали')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands='start')
    dp.register_message_handler(search_command, commands='search')
    dp.register_message_handler(stop_command, commands='stop')
