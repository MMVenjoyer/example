# -*- coding: utf-8 -*-
import asyncio
import logging
import markups as kb
import aiohttp

from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import DataManipulation
from settings import TOKEN


logging.basicConfig(level = logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    product_article = State()


async def get_data_by_article(product_article: int) -> (tuple[str, int, int, float, int]):
	'''Получаем данные по артиклю и конвертированные кортежем возвращаем назад'''
	async with aiohttp.ClientSession() as session:
		async with session.get(f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={product_article}') as result:
			result_status = result.status
			if result_status == 200:
				result = await result.json()
				result = result['data']['products'][0]
				product_name = result['name']
				product_article = result['id']
				product_price = result['salePriceU']
				product_rate = result['reviewRating']
				try:
					product_last = result['sizes'][0]['stocks'][0]['qty']
				except:
					product_last = 0

				return (product_name, product_article, product_price, product_rate, product_last,)
			else:
				return False


async def get_generated_answer(text_to_generate: tuple, status: bool) -> str:
	'''Генерирует ответ по необходимости и в взависимости от возможного количества строк в бд(не больше 5)'''
	if status:
		return f"""
💬Название: {text_to_generate[0]}

🆔Артикул: {text_to_generate[1]}
💸Цена: {str(text_to_generate[2])[:-2]} руб
⭐️Рейтинг: {text_to_generate[3]}
🏢Осталось на складе: {text_to_generate[4]}"""
	
	else:
		answer = ''
		for i in range(len(text_to_generate)):
			answer += f'''

{i+1} Заявка:
ID: {text_to_generate[i].user_id}
Время запроса: {text_to_generate[i].send_time}
Артикль: {text_to_generate[i].product_article}'''
		return answer


####################################################################
# 					ХЭНДЛЕРЫ ОБЫЧНЫХ СООБЩЕНИЙ					   #
####################################################################


@dp.message_handler(commands = ['start'])
async def get_start(message: types.Message):
	await bot.send_message(message.from_user.id, 'Бот для примера кода', reply_markup=kb.kb_menu)


@dp.message_handler(text = ['Получить информацию по товару✳️', 'Получить информацию из БД⏺'])
async def get_main_menu(message: types.Message):
	if message.text == 'Получить информацию по товару✳️': # Получаем инфу по артиклю
		await bot.send_message(message.from_user.id, 'Отправьте мне нужный вам артикул:')
		await UserState.product_article.set()

	elif message.text == 'Получить информацию из БД⏺': # Получаем 5 последних запросов
		result = DataManipulation.get_last_requests(message.from_user.id, 5)
		if len(result) < 1:
			await bot.send_message(message.from_user.id, 'Запросов недостаточно, пожалуйста, введите еще несколько')
		else:
			answer_text = await asyncio.create_task(get_generated_answer(result, False))
			await bot.send_message(message.from_user.id, answer_text)


####################################################################
# 							ХЭНДЛЕРЫ FSM						   #
####################################################################
			

@dp.message_handler(state=UserState.product_article)
async def get_product_article(message: types.Message, state: FSMContext):
	await state.update_data(product_article=message.text)
	state_data = await state.get_data()
	product_article = state_data['product_article']
	if product_article.isdigit() and 7 < len(str(product_article)) < 14:
		result = await asyncio.create_task(get_data_by_article(int(product_article)))
		if result:
			try:
				DataManipulation.write_data(int(message.from_user.id), str(datetime.now()), int(result[1]))
			except:
				print('ошибка добавления')
			answer_text = await asyncio.create_task(get_generated_answer(result, True))
			await bot.send_message(message.from_user.id, answer_text)
		else:
			await bot.send_message(message.from_user.id, "Возникла ошибка на стороне сервера!")
	else:
		await bot.send_message(message.from_user.id, "Вы ввели неправильный артикул!")

	await state.finish()



######################################################################################################################################


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates = True)
