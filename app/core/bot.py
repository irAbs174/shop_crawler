import telebot
from telebot import types
import requests
from html import escape
import schedule
from threading import Thread
import time

# Bot token
TOKEN = "7475255594:AAHW5qXvU9h9LaOHfaZgSRH5618ZhPBLuQQ"
bot = telebot.TeleBot(TOKEN)

def check_api_and_notify():
    try:
        response = requests.post('http://0.0.0.0:8080/api/newLogs').json()
        if response['status'] != ['']:
            print(response['status'])
            for j in response['status']:
                logName = j['logName']
                logType = j['logType']
                res = requests.post('http://0.0.0.0:8080/api/get_chat_id').json()
                for i in res['status']:
                    print(res['status'])
                    print(i)
                    userId = i['chatId']
                    if userId:
                        msg = f"""
                        گزارش جدید خزنده‌ !
                        {logName} \n
                        {logType}
                        """
                        bot.send_message(int(userId),msg)
        else:
            print('noting !')
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")

def job():
    print("Checking API...")
    check_api_and_notify()

# Schedule the job every 100 seconds
schedule.every(60*60*12).seconds.do(job)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# List of authorized usernames
USERNAMES = [
    'Unique174',
    'fghani41',
    'maryamghzh',
    'alireezwwee',
    'saeed1321',
    'EhsanPishyar',
    'Sunaazzz1993',
    'Khakia2424',
    'Toktam_rbj',
]

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username
    userId = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    if username in USERNAMES:
        user = {
            'userId': userId,
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        }
        print(user)
        try:
            response = requests.post("http://0.0.0.0:8080/api/register", data=user)
            response_data = response.json()
            print(f"Registration response: {response_data}")
        except requests.exceptions.RequestException as e:
            print(f"Error during registration: {e}")
            bot.send_message(message.chat.id, "خطایی در ثبت نام رخ داده است.")
            return

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

@bot.message_handler()
def handle_buttons(message):
    print(f"Received button press: {message.text}")
    if message.text == 'محصولات':
        new_buttons = ['مقایسه','برون بری', 'محصولات قیمت بالا', 'محصولات زیر شده', 'محصولات هم قیمت', 'بازگشت']
        new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        new_markup.add(*[types.KeyboardButton(button) for button in new_buttons])
        bot.send_message(message.chat.id, "یک گزینه را انتخاب کنید:", reply_markup=new_markup)
    elif message.text == 'اهداف':
        new_buttons = ['افزودن هدف', 'مشاهده اهداف', 'سایت مرجع', 'بازگشت']
        new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        new_markup.add(*[types.KeyboardButton(button) for button in new_buttons])
        bot.send_message(message.chat.id, "یک گزینه را انتخاب کنید:", reply_markup=new_markup)
    elif message.text == 'گزارشات':
        get_reports(message)
    elif message.text == 'کاربران ربات':
        bot.send_message(message.chat.id, "لیست کاربران ربات:")
        for user in USERNAMES:
            bot.send_message(message.chat.id, user)
    elif message.text == 'بازگشت':
        main_menu(message)
    else:
        handle_product_management(message)

def handle_product_management(message):
    print(f"Handling product management: {message.text}")
    if message.text == 'محصولات قیمت بالا':
        get_us_products(message)
    elif message.text == 'مقایسه':
        try:
            res = requests.post('http://0.0.0.0:8080/api/perform_comparison',{}).json()
            progress_message = bot.send_message(message.chat.id, "در حال مقایسه محصولات لطفاً صبر کنید...")
            bot.send_message(message.chat.id, res['status'])
        except Exception as e:
            bot.send_message(message.chat.id, e)
    elif message.text == 'محصولات زیر شده':
        try:
            res = requests.post('http://0.0.0.0:8080/api/get_down_products_price_api').json()
            print(f"Received down products: {res}")
            if res['status']:
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
            else:
                bot.send_message(message.chat.id, "هنوز کالایی زیر نشده")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            bot.send_message(message.chat.id, "خطایی در دریافت محصولات رخ داده است.")
    elif message.text == 'محصولات هم قیمت':
        get_equals_products(message)
    elif message.text == 'برون بری':
        progress_message = bot.send_message(message.chat.id, "در حال تولید فایل خروجی لطفاً صبر کنید...")
        try:
            with open('Products_Export=>buykif.csv', 'rb') as file:
                bot.send_document(message.chat.id, file, caption="لیست محصولات بای کیف")
            with open('Products_Export=>123kif.csv', 'rb') as file:
                bot.send_document(message.chat.id, file, caption="لیست محصولات یک دو سه کیف")
        except FileNotFoundError as e:
            bot.send_message(message.chat.id, "خطا در ارسال فایل: فایل پیدا نشد.")
    elif message.text == 'بازگشت':
        main_menu(message)
    else:
        product = message.text
        res = requests.post('http://0.0.0.0:8080/api/single_comparison', data={'product_name' : product}).json()
        for i in res['status']:
            name = i['name']
            price = i['price']
            stock = i['stock']
            url = i['url']
            bot.send_message(message.chat.id, f"کالا: {name} \n قیمت: {price} \n آدرس محصول {url} \n موجودی: {stock}")

def get_reports(message):
    print("Fetching reports")
    try:
        response = requests.post('http://0.0.0.0:8080/api/get_logs_api').json()
        count = requests.post('http://0.0.0.0:8080/api/get_count_data').json()
        if response['success']:
            msg = f"""
            \n
            گزارش عملکرد :\n
            تعداد اهداف : {count['status']['all_target_count']} \n
            سایت مرجع : {count['status']['main_target']} \n
            تعداد محصول اسکن شده : {count['status']['all_products_count']} \n
            تعداد محصول زیر قیمت مرجع : {count['status']['down_products_count']} \n
            تعداد محصول هم قیمت مرجع: {count['status']['up_products_count']} \n
            تعداد محصول بالاتر از قیمت مرجع: {count['status']['equals_products_count']} \n\b
            """
            for log in response['status']:
                msg += f"\n{escape(log['name'])} {log['logType']}\n_____________________________ \n"
            bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, "خطایی در دریافت گزارشات رخ داده است.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "خطایی در دریافت گزارشات رخ داده است.")

def get_equals_products(message):
    print("Fetching equals products")
    try:
        res = requests.post('http://0.0.0.0:8080/api/get_equals_products_price_api').json()
        if res['status']:
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
        else:
            bot.send_message(message.chat.id, 'کالای هم قیمت یافت نشد')
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "خطایی در دریافت محصولات رخ داده است.")

def get_us_products(message):
    print("Fetching us products")
    try:
        res = requests.post('http://0.0.0.0:8080/api/get_us_products_api').json()
        if res['status']:
            for i in res['status']:
                name = i['name']
                price = i['price']
                msg = f'''
    نام محصول : {name}
    قیمت : {price}
                '''
                bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, 'کالای با قیمت بالاتر از مرجع یافت نشد')
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "خطایی در دریافت محصولات رخ داده است.")

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
    # Start the scheduling in a separate thread
    schedule_thread = Thread(target=run_schedule)
    schedule_thread.start()
    
    # Start the bot (optional if you want bot interaction)
    bot.infinity_polling()