import asyncio
import logging
import sys
import requests

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from export import export_products
from aiohttp import ClientSession
from openpyxl import Workbook
from html import escape
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
import os

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7475255594:AAHW5qXvU9h9LaOHfaZgSRH5618ZhPBLuQQ"

# Initialize Bot instance with default bot properties which will be passed to all API calls
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))



# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

@dp.callback_query()
async def callback_query_handler(callback_query: CallbackQuery) -> None:
    if callback_query.data == "option1":
        await callback_query.message.answer("/getProducts")

    elif callback_query.data == "option2":
        await callback_query.message.answer("/logs")
    elif callback_query.data == "option3":
        await callback_query.message.answer("/jobs")
    elif callback_query.data == "option4":
        await callback_query.message.answer("/start")

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    USERSNAMES = [
        'Unique174',
        'fghani41',
        '@maryamghzh',
        'alireezwwee',
        '@saeed1321',
    ]

    username = message.from_user.username

    if username in USERSNAMES:
        answer = f"""سلام, {html.bold(message.from_user.full_name)}!
    خوش آمدید.
    برای شروع با پرسیدن یک سوال شروع کنید.
    چه خبر؟
    یا از گزینه های زیر استفاده کنید :
        """
        
        # Create an inline keyboard with buttons
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="محصولات", callback_data="option1")],
            [InlineKeyboardButton(text="گزارشات", callback_data="option2")],
            [InlineKeyboardButton(text="مشاهده کار جاری", callback_data="option3")],
            [InlineKeyboardButton(text="راهنمای ربات", callback_data="option4")]
        ])
    else:
            answer = "شما مجاز به استفاده از ربات نیستید"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="تماس با سازنده", callback_data="none")] ])
        
    await message.answer(answer, reply_markup=keyboard)

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will send a custom message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        print(f'=> {message.chat}')
        print(f'User sent: {message.text}')

        if message.text == '/getProducts':
            progress_message = await message.answer("در حال تولید فایل Excel، لطفاً صبر کنید...")
            async with ClientSession() as session:
                async with session.post('http://0.0.0.0:8080/api/get_products_api') as response:
                    data = await response.json()
                    count = data['count']
                    await message.answer(f"تعداد محصولات : {count} ")
                    products_data = [[
                        'فروشگاه',
                        'نام کالا',
                        'قیمت کالا',
                        'وضعیت',
                        'موجودی',
                        'صفحه محصول',
                    ]]
                    for i in data['status']:
                        print(data['status'])
                        stock = 'ناموجود' if i['price'] == '0' or i['stock'] == 'ناموجود' else 'موجود'
                        products_data.append([
                            i['parent'],
                            i['name'],
                            i['price'],
                            i['status'],
                            stock,
                            i['url'],
                        ])

                    # Create an Excel workbook and add the data
                    wb = Workbook()
                    ws = wb.active
                    for row in products_data:
                        print(row)
                        ws.append(row)
                    
                    file_path = 'products.xlsx'
                    wb.save(file_path)
                    file = FSInputFile('products.xlsx')
                    await bot.send_document(chat_id=message.chat.id, document=file, caption="لیست محصولات")
                    
                    await progress_message.edit_text("فایل Excel ایجاد شد.")
        elif message.text == '/logs':
            async with ClientSession() as session:
                async with session.post('http://0.0.0.0:8080/api/get_logs_api') as response:
                    logs = await response.json()
                    if logs['success']:
                        msg = "آخرین گزارشات:\n"
                        for log in logs['status']:
                            msg += f"{escape(log['name'])}: {escape(log['logType'])}\n"
                        await bot.send_message(message.chat.id, msg)
                    else:
                        await bot.send_message(message.chat.id, "خطایی در دریافت گزارشات رخ داده است.")
        else:
            await bot.send_message(chat_id=message.chat.id, text=f"{escape(message.text)}")
        await bot.send_message(chat_id=message.chat.id, text=f"{message.text}")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

async def print_love_periodically():
    while True:
        print("Bot start to comparison !!!")
        response = requests.post('http://0.0.0.0:8080/api/perform_comparison', {}).json()
        for i in response['results']:
            context = i['context']
            if i['status'] == 'down':
                await bot.send_message(chat_id=5507021431, text=context)
            else:
            #7475255594
                print(response)
        
async def main() -> None:
    # Start the periodic task
    asyncio.create_task(print_love_periodically())
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())