import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aiogram import Bot, Dispatcher, executor, types
import re
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))
SMTP_LOGIN = os.getenv('SMTP_LOGIN')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def send_email_secure(recipient_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_LOGIN
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Ошибка отправки письма: {e}")
        return False

user_state = {}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_state[user_id] = {'step': 'waiting_for_email'}
    await message.reply("Отправьте ваш email")

@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_state:
        await message.reply("Начните с команды /start.")
        return

    state = user_state[user_id]
    if state['step'] == 'waiting_for_email':
        if is_valid_email(message.text):
            state['email'] = message.text
            state['step'] = 'waiting_for_message'
            await message.reply("Ваш email принят. Теперь отправьте текст сообщения.")
        else:
            await message.reply("Некорректный email. Попробуйте снова.")
    elif state['step'] == 'waiting_for_message':
        email = state['email']
        text_message = message.text
        if send_email_secure(email, "Сообщение от Telegram бота", text_message):
            await message.reply("Сообщение успешно отправлено на ваш email!")
        else:
            await message.reply("Не удалось отправить сообщение.")
        user_state.pop(user_id, None)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)