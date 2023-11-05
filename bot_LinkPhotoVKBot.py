import telebot
import requests
import json
import base64

API_TOKEN = '6905257183:AAG8iNt0PG3qVaDY5qkFP8MWVRHKKjvxanA'
IMGBB_API_ENDPOINT = 'https://api.imgbb.com/1/upload'
IMGBB_API_KEY = '6484c0f651cf789c0a9d5ca047c5c671'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: message.text == '/start')
def start(message):
    response = "<b>📸 Welcome to upload bot!</b>\n\n<i>✅ You can upload your photo and get a URL for your photo</i>\n\nℹ️ Send Photo to upload"
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Master Dev", url='https://t.me/MasterDev01'))
    bot.send_message(message.chat.id, response, parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo_array = message.photo
    photo_id = photo_array[-1].file_id
    photo_file = get_photo_file(photo_id)

    if photo_file:
        imgbb_url = upload_to_imgbb(photo_file)

        if imgbb_url:
            bot.send_message(message.chat.id, f"<b>🎑Image >> {imgbb_url}</b>", parse_mode='HTML', reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, "Failed to upload the photo to ImgBB.")
    else:
        bot.send_message(message.chat.id, "Failed to retrieve the photo.")

def get_photo_file(photo_id):
    file_info = bot.get_file(photo_id)
    photo_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
    return photo_url

def upload_to_imgbb(photo_file):
    post_data = {
        'key': IMGBB_API_KEY,
        'image': base64.b64encode(requests.get(photo_file).content).decode('utf-8')
    }
    response = requests.post(IMGBB_API_ENDPOINT, data=post_data)
    result = response.json()

    if 'data' in result and 'url' in result['data']:
        return result['data']['url']

    return None

if __name__ == '__main__':
    bot.polling()