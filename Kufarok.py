import httpx
from bs4 import BeautifulSoup
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
import config


TIMEOUT = 30  # Задержка перед поиском новых товаров


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

search_dict = {}


@dp.message_handler(commands=['start'])
async def start_message(message: types.message):
    await message.answer('Привет, я написан радиком, для начала моей работы напиши команду /search и укажи что хочешь искать. Пример: /search Мозги радика\nДля остановки поиска воспользуйся /stop\n Бот показывает лишь новые поступающие предложения')


@dp.message_handler(commands=['search'])
async def search(message: types.message):
    try:
        search_dict[message.from_id].close()
        search_dict.pop(message.from_id)
    except:
        pass
    if (message.text == '/search'):
        await message.answer('Вы не написали тему для поиска')
    else:
        search_dict[message.from_id] = checking(message)
        await search_dict[message.from_id]


async def checking(message):
    tag = str(message.text)
    tag = tag[8:]
    last_item = ''
    print('[LOG:] '+tag)
    while (True):
        async with httpx.AsyncClient() as client:
            r = await client.get('https://www.kufar.by/l?cmp=0&query='+tag+'&sort=lst.d')
        if (r.status_code == 200):
            soup = BeautifulSoup(r.text, 'html.parser')
            variants = soup.find('div', class_='styles_cards___qpff')
            products = variants.find_all('section')
            i = 0
            while (products[i].find('a', class_='styles_polepos__bO53x') != None):
                i = i+1
            product = products[i]
            url = product.find('a', class_='styles_wrapper__yaLfq').get('href')
            url = url.split('?')[0]
            price = product.find('div', class_='styles_top__HNf3a').find(
                'p', class_='styles_price__9JZaB').find('span').text
            name = product.find('h3', class_='styles_title__ARIVF').text
            image = product.find('div', class_='styles_container__dR7XZ').find('img')[
                'data-src']
            state = product.find(
                'div', class_='styles_secondary__NEYhw').find('p').text
            if not (url == last_item):
                last_item = url
                print('[LOG:] '+url)
                await message.answer_photo(photo=image, caption='Название: '+name+'\nЦена: '+price+'\nг. '+state+'\nПодробнее:\n'+url)
            await asyncio.sleep(TIMEOUT)


@dp.message_handler(commands=['stop'])
async def stop(message: types.message):
    try:
        search_dict[message.from_id].close()
        search_dict.pop(message.from_id)
        await message.answer('Поиск остановлен')
    except KeyError:
        await message.answer('Вы ничего не искали')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
