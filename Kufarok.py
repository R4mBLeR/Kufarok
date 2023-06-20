import requests
from bs4 import BeautifulSoup 
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
import config


TIMEOUT=3 #Задержка между проверками


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

search_dict = {}

@dp.message_handler(commands=['start'])
async def start_message(message: types.message):
    await message.answer("Привет, я написан радиком, для начала моей работы напиши команду /search и укажи что хочешь искать. Пример: /search Мозги радика")

@dp.message_handler(commands=['search'])
async def search(message : types.message):  
    try:
        search_dict[message.from_id].close()
        search_dict.pop(message.from_id)
    except:
        await message.answer("Какая-то ошибка, кажется я сломался(((((")
    search_dict[message.from_id] = checking(message)
    await search_dict[message.from_id]

   
async def checking(message):
    tag=str(message.text)
    tag=tag[8:]
    last_item =""
    while (True):  
        page = requests.get("https://www.kufar.by/l?cmp=0&query="+tag+"&sort=lst.d")
        if (page.status_code==200):
            soup = BeautifulSoup(page.text, "html.parser")
            product = soup.find('div', class_='styles_cards___qpff').find('a', class_="styles_wrapper__yaLfq").find('div', class_='styles_content__BDDGV')
            price=product.find('div',class_='styles_top__HNf3a').find('p',class_='styles_price__9JZaB').find('span').text
            name=product.find('h3',class_='styles_title__ARIVF').text
            url = soup.find('div', class_='styles_cards___qpff').find('a', class_="styles_wrapper__yaLfq").get('href')
            url = url[0:35]
            if not (url==last_item):
                last_item=url
                await message.answer("Название: "+name+"\n Цена "+price+"\n"+url)
            await asyncio.sleep(TIMEOUT)
        

@dp.message_handler(commands=['stop'])
async def stop(message : types.message):
    try:
        search_dict[message.from_id].close()
        search_dict.pop(message.from_id)
        await message.answer("Поиск остановлен")
    except KeyError:
        await message.answer("Вы ничего не искали")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)