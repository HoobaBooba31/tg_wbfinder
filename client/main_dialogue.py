from aiogram import Router
from aiogram import types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from server import WBfinder
from aiogram.filters import Command
import time
import httpx
import asyncio

keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Начать поиск"),
                                        KeyboardButton(text="Помощь")]],
                                        resize_keyboard=True)

class BotStates(StatesGroup):
    Searching = State()
    Results = State()

ls_router = Router()

@ls_router.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Добро пожаловать в бот для поиска товаров на Wildberries!\n\n" \
                        "Нажмите 'Начать поиск', чтобы начать.", reply_markup=keyboard) 
    
@ls_router.message(F.text == "Начать поиск")
async def start_search(message: types.Message, state: FSMContext):
    await message.answer("Введите название товара для поиска:" \
    "Если вы хотите отменить поиск, просто введите /cancel.")
    await state.set_state(BotStates.Searching)

@ls_router.message(BotStates.Searching)
async def count_pages(message: types.Message, state: FSMContext):

    if message.text == '/cancel':
        await state.clear()
        await message.answer("Поиск отменён. Если хотите начать заново, нажмите 'Начать поиск'.")
        return
    
    search_query = message.text
    await state.update_data(search_query=search_query)
    await message.answer("Сколько страниц результатов вы хотите получить? (Введите число):")
    await state.set_state(BotStates.Results)

@ls_router.message(BotStates.Results)
async def perform_search(message: types.Message, state: FSMContext):
    if message.text == '/cancel':
        await state.clear()
        await message.answer("Поиск отменён. Если хотите начать заново, нажмите 'Начать поиск'.")
        return
    try:
        page_count = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для количества страниц.")
        return

    user_data = await state.get_data()
    search_query = user_data.get('search_query')

    await message.answer(f"Ищем '{search_query}' на {page_count} страницах...")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"http://server:8000/search?query={search_query}&pages={page_count}")
            data = resp.json()
            results = data['results']
    except:
        await message.answer('Вышла какая-то ошибка, попробуйте снова')
        await state.clear()
        return
    
    if not results:
        await message.answer("По вашему запросу ничего не найдено.")
    else:
        for item in range(len(results)):
            await message.answer(f"{results[item]['name']}\n{results[item]['url']}")
            if item % 50 == 0:
                time.sleep(10)


    await state.clear()


# async def check(query: str):
