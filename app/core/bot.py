import telebot
from telebot import types
import requests
from html import escape
import schedule
from threading import Thread
import time
from core.sec import *

# Bot token
TOKEN = TELEGRAM_BOT_TOKEN 
bot = telebot.TeleBot(TOKEN)

def check_api_and_notify():
    try:
        response = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/newLogs').json()
        if response['status'] != ['']:
            print(response['status'])
            for j in response['status']:
                logName = j['logName']
                logType = j['logType']
                lastLog = j['lastLog']
                res = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/get_chat_id').json()
                for i in res['status']:
                    print(res['status'])
                    print(i)
                    userId = i['chatId']
                    if userId:
                        msg = f"""
                        Ú¯Ø²Ø§Ø±Ø´ Ø¬Ø¯ÛŒØ¯ Ø®Ø²Ù†Ø¯Ù‡â€Œ !
                        {logName} \n
                        {logType} \n
                        {lastLog}
                        """
                        bot.send_message(int(userId),msg)
        else:
            print('noting !')
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")

def job():
    print("Checking for new notifications...")
    check_api_and_notify()

# Schedule the job every 100 seconds
schedule.every(120).seconds.do(job)

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
            response = requests.post(f"http://{DJANGO_HOST}:{DJANGO_PORT}/api/register", data=user)
            response_data = response.json()
            print(f"Registration response: {response_data}")
        except requests.exceptions.RequestException as e:
            print(f"Error during registration: {e}")
            bot.send_message(message.chat.id, "Ø®Ø·Ø§ÛŒÛŒ Ø¯Ø± Ø«Ø¨Øª Ù†Ø§Ù… Ø±Ø® Ø¯Ø§Ø¯Ù‡ Ø§Ø³Øª.")
            return

        answer = f"Ø³Ù„Ø§Ù…, <b>{escape(message.from_user.full_name)}</b>! Ø®ÙˆØ´ Ø¢Ù…Ø¯ÛŒØ¯."
        bot.send_message(message.chat.id, answer, parse_mode='HTML')
        main_menu(message)
    else:
        bot.send_message(message.chat.id, 'Ø´Ù…Ø§ Ù…Ø¬Ø§Ø² Ø¨Ù‡ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² Ø±Ø¨Ø§Øª Ù†ÛŒØ³ØªÛŒØ¯')

def main_menu(message):
    buttons = [
        'Ù…Ø­ØµÙˆÙ„Ø§Øª',
        'Ø§Ù‡Ø¯Ø§Ù',
        'Ú¯Ø²Ø§Ø±Ø´Ø§Øª',
        'Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ú©Ø§Ø± Ø¬Ø§Ø±ÛŒ',
        'Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø±Ø¨Ø§Øª',
    ]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*[types.KeyboardButton(button) for button in buttons])
    bot.send_message(message.chat.id, "Ù„Ø·ÙØ§ ÛŒÚ© Ú¯Ø²ÛŒÙ†Ù‡ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯", reply_markup=markup)

@bot.message_handler()
def handle_buttons(message):
    print(f"Received button press: {message.text}")
    if message.text == 'Ù…Ø­ØµÙˆÙ„Ø§Øª':
        new_buttons = ['Ù…Ù‚Ø§ÛŒØ³Ù‡','Ø¨Ø±ÙˆÙ† Ø¨Ø±ÛŒ', 'Ù…Ø­ØµÙˆÙ„Ø§Øª Ù‚ÛŒÙ…Øª Ø¨Ø§Ù„Ø§', 'Ù…Ø­ØµÙˆÙ„Ø§Øª Ø²ÛŒØ± Ø´Ø¯Ù‡', 'Ù…Ø­ØµÙˆÙ„Ø§Øª Ù‡Ù… Ù‚ÛŒÙ…Øª', 'Ø¨Ø§Ø²Ú¯Ø´Øª']
        new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        new_markup.add(*[types.KeyboardButton(button) for button in new_buttons])
        bot.send_message(message.chat.id, "ÛŒÚ© Ú¯Ø²ÛŒÙ†Ù‡ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=new_markup)
    elif message.text == 'Ø§Ù‡Ø¯Ø§Ù':
        new_buttons = ['Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø§Ù‡Ø¯Ø§Ù', 'Ø³Ø§ÛŒØª Ù…Ø±Ø¬Ø¹', 'Ø¨Ø§Ø²Ú¯Ø´Øª']
        new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        new_markup.add(*[types.KeyboardButton(button) for button in new_buttons])
        bot.send_message(message.chat.id, "ÛŒÚ© Ú¯Ø²ÛŒÙ†Ù‡ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=new_markup)
    elif message.text == 'Ú¯Ø²Ø§Ø±Ø´Ø§Øª':
        get_reports(message)
    elif message.text == 'Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø±Ø¨Ø§Øª':
        bot.send_message(message.chat.id, "Ù„ÛŒØ³Øª Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø±Ø¨Ø§Øª:")
        for user in USERNAMES:
            bot.send_message(message.chat.id, user)
    elif message.text == 'Ø³Ø§ÛŒØª Ù…Ø±Ø¬Ø¹':
        get_main_target(message)
    elif message.text == 'Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø§Ù‡Ø¯Ø§Ù':
        get_target_api(message)
    elif message.text == 'Ø¨Ø§Ø²Ú¯Ø´Øª':
        main_menu(message)
    else:
        handle_product_management(message)

def handle_product_management(message):
    print(f"Handling product management: {message.text}")
    if message.text == 'Ù…Ø­ØµÙˆÙ„Ø§Øª Ù‚ÛŒÙ…Øª Ø¨Ø§Ù„Ø§':
        get_up_products(message)
    elif message.text == 'Ù…Ù‚Ø§ÛŒØ³Ù‡':
        get_preform_comparison(message)
    elif message.text == 'Ù…Ø­ØµÙˆÙ„Ø§Øª Ø²ÛŒØ± Ø´Ø¯Ù‡':
        get_down_products(message)
    elif message.text == 'Ù…Ø­ØµÙˆÙ„Ø§Øª Ù‡Ù… Ù‚ÛŒÙ…Øª':
        get_equals_products(message)
    elif message.text == 'Ø¨Ø±ÙˆÙ† Ø¨Ø±ÛŒ':
        get_export_products(message)
    elif message.text == 'Ø¨Ø§Ø²Ú¯Ø´Øª':
        main_menu(message)
    else:
        search(message)


def get_preform_comparison(message):
    try:
        res = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/perform_comparison',{}).json()
        progress_message = bot.send_message(message.chat.id, "Ø¯Ø± Ø­Ø§Ù„ Ù…Ù‚Ø§ÛŒØ³Ù‡ Ù…Ø­ØµÙˆÙ„Ø§Øª Ù„Ø·ÙØ§Ù‹ ØµØ¨Ø± Ú©Ù†ÛŒØ¯...")
        bot.send_message(message.chat.id, res['status'])
    except Exception as e:
        bot.send_message(message.chat.id, e)

def search(message):
    product = message.text
    res = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/single_comparison', data={'product_name' : product}).json()
    for i in res['status']:
        name = i['name']
        price = i['price']
        stock = i['stock']
        url = i['url']
        bot.send_message(message.chat.id, f"Ú©Ø§Ù„Ø§: {name} \n Ù‚ÛŒÙ…Øª: {price} \n Ø¢Ø¯Ø±Ø³ Ù…Ø­ØµÙˆÙ„ {url} \n Ù…ÙˆØ¬ÙˆØ¯ÛŒ: {stock}")

def get_export_products(message):
    progress_message = bot.send_message(message.chat.id, "Ø¯Ø± Ø­Ø§Ù„ ØªÙˆÙ„ÛŒØ¯ ÙØ§ÛŒÙ„ Ø®Ø±ÙˆØ¬ÛŒ Ù„Ø·ÙØ§Ù‹ ØµØ¨Ø± Ú©Ù†ÛŒØ¯...")
    try:
        with open('Products_Export=>buykif.csv', 'rb') as file:
            bot.send_document(message.chat.id, file, caption="Ù„ÛŒØ³Øª Ù…Ø­ØµÙˆÙ„Ø§Øª Ø¨Ø§ÛŒ Ú©ÛŒÙ")
        with open('Products_Export=>123kif.csv', 'rb') as file:
            bot.send_document(message.chat.id, file, caption="Ù„ÛŒØ³Øª Ù…Ø­ØµÙˆÙ„Ø§Øª ÛŒÚ© Ø¯Ùˆ Ø³Ù‡ Ú©ÛŒÙ")
        with open('Export_All.csv', 'rb') as file:
            bot.send_document(message.chat.id, file, caption="All Products")
    except FileNotFoundError as e:
        with open('Export_All.csv', 'rb') as file:
            bot.send_document(message.chat.id, file, caption="All Products")

def get_main_target(message):
    response = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/get_main_target').json()
    bot.send_message(message.chat.id, f"Ø³Ø§ÛŒØª Ù…Ø±Ø¬Ø¹ : {response['status']}")

def get_target_api(message):
    response = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/get_target_api').json()
    for i in response['status']:
        count = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/get_target_products_count', data={'url': i['url']}).json()
        bot.send_message(message.chat.id, f"Ù†Ø§Ù… Ø³Ø§ÛŒØª: {i['name']} \n Ø¢Ø¯Ø±Ø³: {i['url']} \n ØªØ¹Ø¯Ø§Ø¯ Ù…Ø­ØµÙˆÙ„Ø§Øª: {count['all_target_products_count']} ØªØ¹Ø¯Ø§Ø¯ Ù…Ø­ØµÙˆÙ„Ø§Øª Ù…ÙˆØ¬ÙˆØ¯:â€Œ {count['stock_count']}, ØªØ¹Ø¯Ø§Ø¯ Ù…Ø­ØµÙˆÙ„Ø§Øª Ù†Ø§Ù…ÙˆØ¬ÙˆØ¯: {count['out_stock_count']}")

def get_reports(message):
    try:
        response = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/get_logs_api').json()
        count = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/get_count_data').json()
        if response['success']:
            msg = f"""
            \n
            Ú¯Ø²Ø§Ø±Ø´ Ø¹Ù…Ù„Ú©Ø±Ø¯ :\n
            ØªØ¹Ø¯Ø§Ø¯ Ø§Ù‡Ø¯Ø§Ù : {count['status']['all_target_count']} \n
            Ø³Ø§ÛŒØª Ù…Ø±Ø¬Ø¹ : {count['status']['main_target']} \n
            ØªØ¹Ø¯Ø§Ø¯ Ù…Ø­ØµÙˆÙ„ Ø§Ø³Ú©Ù† Ø´Ø¯Ù‡ : {count['status']['all_products_count']} \n
            ØªØ¹Ø¯Ø§Ø¯ Ù…Ø­ØµÙˆÙ„ Ø²ÛŒØ± Ù‚ÛŒÙ…Øª Ù…Ø±Ø¬Ø¹ : {count['status']['down_products_count']} \n
            ØªØ¹Ø¯Ø§Ø¯ Ù…Ø­ØµÙˆÙ„ Ù‡Ù… Ù‚ÛŒÙ…Øª Ù…Ø±Ø¬Ø¹: {count['status']['up_products_count']} \n
            ØªØ¹Ø¯Ø§Ø¯ Ù…Ø­ØµÙˆÙ„ Ø¨Ø§Ù„Ø§ØªØ± Ø§Ø² Ù‚ÛŒÙ…Øª Ù…Ø±Ø¬Ø¹: {count['status']['equals_products_count']} \n\b
            """
            for log in response['status']:
                msg += f"\n{escape(log['name'])} {log['logType']}\n Ø²Ù…Ø§Ù† Ø«Ø¨Øª Ú¯Ø²Ø§Ø±Ø´: {log['lastLog']}\n_____________________________ \n"
            bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, "Ø®Ø·Ø§ÛŒÛŒ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ú¯Ø²Ø§Ø±Ø´Ø§Øª Ø±Ø® Ø¯Ø§Ø¯Ù‡ Ø§Ø³Øª.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Ø®Ø·Ø§ÛŒÛŒ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ú¯Ø²Ø§Ø±Ø´Ø§Øª Ø±Ø® Ø¯Ø§Ø¯Ù‡ Ø§Ø³Øª.")

def get_down_products(message):
    try:
        res = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/get_down_products_price_api').json()
        print(f"Received down products: {res}")
        if res['status']:
            for i in res['status']:
                logName = i['logName']
                logType = i['logType']
                lastLog = i['lastLog']
                msg = f'''
                {logName} \n
                {logType} \n
                {lastLog}
                '''
                bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, "Ù‡Ù†ÙˆØ² Ú©Ø§Ù„Ø§ÛŒÛŒ Ø²ÛŒØ± Ù†Ø´Ø¯Ù‡")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Ø®Ø·Ø§ÛŒÛŒ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù…Ø­ØµÙˆÙ„Ø§Øª Ø±Ø® Ø¯Ø§Ø¯Ù‡ Ø§Ø³Øª.")
        
def get_equals_products(message):
    print("Fetching equals products")
    try:
        res = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/get_equals_products_price_api').json()
        if res['status']:
            for i in res['status']:
                logName = i['logName']
                logType = i['logType']
                lastLog = i['lastLog']
                msg = f'''
                {logName} \n
                {logType} \n
                {lastLog}
                '''
                bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, 'Ú©Ø§Ù„Ø§ÛŒ Ù‡Ù… Ù‚ÛŒÙ…Øª ÛŒØ§ÙØª Ù†Ø´Ø¯')
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Ø®Ø·Ø§ÛŒÛŒ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù…Ø­ØµÙˆÙ„Ø§Øª Ø±Ø® Ø¯Ø§Ø¯Ù‡ Ø§Ø³Øª.")

def get_up_products(message):
    print("Fetching us products")
    try:
        res = requests.post(f'http://{DJANGO_HOST}:{DJANGO_PORT}/api/get_normal_products_price_api').json()
        if res['status']:
            for i in res['status']:
                logName = i['logName']
                logType = i['logType']
                lastLog = i['lastLog']
                msg = f'''
                {logName} \n
                {logType} \n
                {lastLog}
                '''
                bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, 'Ú©Ø§Ù„Ø§ÛŒ Ø¨Ø§ Ù‚ÛŒÙ…Øª Ø¨Ø§Ù„Ø§ØªØ± Ø§Ø² Ù…Ø±Ø¬Ø¹ ÛŒØ§ÙØª Ù†Ø´Ø¯')
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Ø®Ø·Ø§ÛŒÛŒ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù…Ø­ØµÙˆÙ„Ø§Øª Ø±Ø® Ø¯Ø§Ø¯Ù‡ Ø§Ø³Øª.")


if __name__ == '__main__':
    # Start the scheduling in a separate thread
    schedule_thread = Thread(target=run_schedule)
    schedule_thread.start()
    
    # Start the bot (optional if you want bot interaction)
    bot.infinity_polling()