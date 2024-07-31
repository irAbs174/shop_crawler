import telebot
from telebot import types
import requests
from html import escape

# Bot token
TOKEN = "7475255594:AAHW5qXvU9h9LaOHfaZgSRH5618ZhPBLuQQ"
bot = telebot.TeleBot(TOKEN)

# List of authorized usernames
USERSNAMES = [
    'Unique174',
    'fghani41',
    'maryamghzh',
    'alireezwwee',
    'saeed1321',
    'EhsanPishyar',
    'Sunaazzz1993',
    'Khakia2424'
]

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username
    userId = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    if username in USERSNAMES:
        user = {
            'userId' : userId,
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        }
        response = requests.post("http://0.0.0.0:8080/api/register", user)
        print(response.json())
        answer = f"سلام, <b>{escape(message.from_user.full_name)}</b>! خوش آمدید."
        bot.send_message(message.chat.id, answer, parse_mode='HTML')
        main_menu(message)
    else:
        bot.send_message(message.chat.id, 'شما مجاز به استفاده از ربات نیستید')

def main_menu(message):
    buttons = [
        'محصولات',
        'اهداف',
        'گزارشات',
        'مشاهده کار جاری',
        'کاربران ربات',
    ]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*[types.KeyboardButton(button) for button in buttons])
    bot.send_message(message.chat.id, "لطفا یک گزینه انتخاب کنید", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['برون بری', 'محصولات','اهداف','گزارشات','مشاهده کار جاری','کاربران ربات','بازگشت'])
def handle_buttons(message):
    if message.text == 'محصولات':
        new_buttons = ['برون بری', 'محصولات قیمت بالا','محصولات زیر شده', 'محصولات هم قیمت', 'محصولات تحت نظر', 'بازگشت']
        new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        new_markup.add(*[types.KeyboardButton(button) for button in new_buttons])
        bot.send_message(message.chat.id, "یک گزینه را انتخاب کنید:", reply_markup=new_markup)
    elif message.text == 'اهداف':
        new_buttons = ['افزودن هدف', 'مشاهده اهداف', 'سایت مرجع', 'بازگشت']
        new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        new_markup.add(*[types.KeyboardButton(button) for button in new_buttons])
        bot.send_message(message.chat.id, "یک گزینه را انتخاب کنید:", reply_markup=new_markup)
    elif message.text == 'گزارشات':
        new_buttons = ['گزارشات اسکن', 'بازگشت']
        new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        new_markup.add(*[types.KeyboardButton(button) for button in new_buttons])
        bot.send_message(message.chat.id, "یک گزینه را انتخاب کنید:", reply_markup=new_markup)
    elif message.text == 'مشاهده کار جاری':
        bot.send_message(message.chat.id, "در حال حاضر کار جاری نداریم!")
    elif message.text == 'کاربران ربات':
        bot.send_message(message.chat.id, "لیست کاربران ربات:")
        for user in USERSNAMES:
            bot.send_message(message.chat.id, user)
    elif message.text == 'بازگشت':
        main_menu(message)
    else:
        handle_product_management(message)

def handle_logs_management(message):
    if message.text == 'گزارشات اسکن':
        get_reports(message)
    elif message.text == 'بازگشت':
        main_menu(message)
    else:
        bot.send_message(message.chat.id, "دستور نامعتبر است.")

def handle_product_management(message):
    if message.text == 'محصولات قیمت بالا':
        get_reports(message)
    elif message.text == 'محصولات زیر شده':
        get_down_products(message)
    elif message.text == 'محصولات هم قیمت':
        get_equals_products(message)
    elif message.text == 'محصولات تحت نظر':
        get_us_products(message)
    elif message.text == 'برون بری':
            progress_message = bot.send_message(message.chat.id, "در حال تولید فایل Excel، لطفاً صبر کنید...")
            file = open('products.xlsx', 'rb')
            bot.send_document(message.chat.id, file, caption="لیست محصولات")
    elif message.text == 'بازگشت':
        main_menu(message)
    else:
        bot.send_message(message.chat.id, "دستور نامعتبر است.")

def get_reports(message):
    response = requests.post('http://0.0.0.0:8080/api/get_logs_api').json()
    if response['success']:
        msg = "آخرین گزارشات:\n"
        for log in response['status']:
            msg += f"{escape(log['name'])}: {escape(log['logType'])}\n"
        bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, "خطایی در دریافت گزارشات رخ داده است.")

def get_down_products(message):
    res = requests.post('http://0.0.0.0:8080/api/get_down_products_price_api').json()
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
        bot.send_message(message.chat.id, msg)

def get_equals_products(message):
    res = requests.post('http://0.0.0.0:8080/api/get_equals_products_price_api').json()
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
        bot.send_message(message.chat.id, msg)

def get_us_products(message):
    res = requests.post('http://0.0.0.0:8080/api/get_us_products_api').json()
    for i in res['status']:
        name = i['name']
        price = i['price']
        msg = f'''
نام محصول : {name}
قیمت : {price}
        '''
        bot.send_message(message.chat.id, msg)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    bot.send_message(message.chat.id, "فایل دریافت شد!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "تصویر دریافت شد!")

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data == 'inline_button_1':
        bot.send_message(call.message.chat.id, "شما دکمه Inline Button 1 را کلیک کردید!")
    elif call.data == 'inline_button_2':
        bot.send_message(call.message.chat.id, "شما دکمه Inline Button 2 را کلیک کردید!")

if __name__ == '__main__':
    bot.infinity_polling()
