from dp_init import dp
from handlers import utils
from aiogram import types


async def start_command(message: types.message):
    await message.answer('Привет, я написан радиком, для начала моей работы напиши команду /search и укажи что хочешь искать. Пример: /search Мозги радика\nДля остановки поиска воспользуйся /stop\n Бот показывает лишь новые поступающие предложения')


async def search_command(message: types.message):
    try:
        utils.search_dict[message.from_id].close()
        utils.search_dict.pop(message.from_id)
    except:
        pass
    if (message.text == '/search'):
        await message.answer('Вы не написали тему для поиска')
    else:
        utils.search_dict[message.from_id] = utils.checking(message)
        await utils.search_dict[message.from_id]


async def stop_command(message: types.message):
    try:
        utils.search_dict[message.from_id].close()
        utils.search_dict.pop(message.from_id)
        await message.answer('Поиск остановлен')
    except KeyError:
        await message.answer('Вы ничего не искали')
