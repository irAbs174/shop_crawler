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
        msg = '''
        لیست دستورات ربات :
        1. افزودن کالای تحت نظر
        2. گزارش
        3. خروجی محصولات
        4. محصولات زیر شده
        5. محصولات هم قیمت
        6. کار جاری
        7. مشاهده محصولات تحت نظر 
        '''
        await callback_query.message.answer(msg)

    elif callback_query.data == "option2":
        await callback_query.message.answer("تایپ کنید: گزارش")
    elif callback_query.data == "option3":
        await callback_query.message.answer("تایپ کنید: کار جاری")
    elif callback_query.data == "option4":
        await callback_query.message.answer("تایپ کنید: راهنما")

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = {
        'userId': message.chat.id,
        'username': message.fromuser.username,
        'first_name': message.fromuser.first_name,
        'last_name': message.fromuser.last_name,
    }
    res = requests.post('http://0.0.0.0:8080/api/register').json()

    print(res['status'])
    
    USERSNAMES = [
        'Unique174',
        'fghani41',
        '@maryamghzh',
        'alireezwwee',
        '@saeed1321',
        'EhsanPishyar',
        'Khakia2424'
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
            [InlineKeyboardButton(text="لیست دستورات", callback_data="option1")],
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

        if message.text == 'خروجی':
            progress_message = await message.answer("در حال تولید فایل Excel، لطفاً صبر کنید...")
            async with ClientSession() as session:
                file = FSInputFile('products.xlsx')
                await bot.send_document(chat_id=message.chat.id, document=file, caption="لیست محصولات")
        elif message.text == 'گزارش':
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
        elif message.text == 'افزودن کالای تحت نظر':
            msg = '''
            فرمت اصلی :‌افزودن:کالا:قیمت
            برای افزودن کالای هدف مطابق نمونه عمل کنید :
            افزودن:fclt10:250000
            '''
            progress_message = await message.answer(msg)
        elif 'افزودن:' in message.text:
            name = message.text.split(':')[1]
            price = message.text.split(':')[2]
            print(name, price)
            context = {'name': name, 'price': price}
            response = requests.post('http://0.0.0.0:8080/api/add_us_products_api', context).json()
            msg = f'''
            کالای {name} با قیمت {price} تحت نظر قرار گرفت
            '''
            progress_message = await message.answer(msg)
        elif 'محصولات زیر شده' in message.text:
            res = requests.post('http://0.0.0.0:8080/api/get_down_products_price_api', {}).json()
            context = []
            for i in res['status']:
                name = i['name']
                price = i['price']
                stock = i['stock']
                url = i['url']
                parent = i['parent']

                msg = f'''
                نام محصول : {name}
                قیمت : {price}
                وضعیت موجودی : {stock}
                آدرس صفحه محصول : {url}
                فروشگاه : {parent}
                '''
                await message.answer(msg)
        elif 'محصولات هم قیمت' in message.text:
            res = requests.post('http://0.0.0.0:8080/api/get_equals_products_price_api', {}).json()
            context = []
            for i in res['status']:
                name = i['name']
                price = i['price']
                stock = i['stock']
                url = i['url']
                parent = i['parent']

                msg = f'''
                نام محصول : {name}
                قیمت : {price}
                وضعیت موجودی : {stock}
                آدرس صفحه محصول : {url}
                فروشگاه : {parent}
                '''
                await message.answer(msg)
        elif 'مشاهده محصولات تحت نظر' in message.text:
            res = requests.post('http://0.0.0.0:8080/api/get_us_products_api', {}).json()
            context = []
            for i in res['status']:
                name = i['name']
                price = i['price']
                msg = f'''
                نام محصول : {name}
                قیمت : {price}
                '''
                await message.answer(msg)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
        
async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    for i in range(600):
        print(f"=> BOT ON SLEEP FOR ({i}) secend ...")
        time.sleep(1)