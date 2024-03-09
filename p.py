import telebot
import requests

# Токен вашего бота
TOKEN = '6965501919:AAE8fjKfujY62UYesHIo8JzzxWOkMLWcdU8'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправьте мне IP или координаты (широту и долготу), и я пришлю вам карту местоположения.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Проверяем количество точек в сообщении
        if message.text.count('.') == 2:  
            # Если точек две, предполагаем, что это координаты
            latitude, longitude = map(float, message.text.split())
            bot.send_location(message.chat.id, latitude, longitude)
        else:
            # Иначе, предполагаем, что это IP-адрес
            response = requests.get(f'http://ip-api.com/json/{message.text}')
            data = response.json()
            if data['status'] == 'success':
                latitude = data['lat']
                longitude = data['lon']
                bot.send_location(message.chat.id, latitude, longitude)
            else:
                raise Exception('Ошибка при определении местоположения по IP')
        
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Запуск бота
bot.polling()
