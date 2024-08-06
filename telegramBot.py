import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models import create_tables, Users, Facts, Words

# подключение к базе PostgreSQL
DSN = 'postgresql://postgres:123@localhost:5432/my_music_site'

engine = sqlalchemy.create_engine(DSN)

# #создание объектов
#create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

API_TOKEN = '<YOUR_TOKEN>'

bot = telebot.TeleBot(API_TOKEN)

class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'
    STOP = 'Ну уж нет!'
    LEARN = 'Учиться!'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"""\
    Привет, {message.from_user.first_name} 👋 
    Давай попрактикуемся в английском языке. Тренировки можешь проходить в удобном для себя темпе.
    У тебя есть возможность использовать тренажёр, как конструктор, и собирать свою собственную базу для обучения. Для этого воспрользуйся инструментами:
    добавить слово ➕,
    удалить слово 🔙.
    Ну что, начнём ⬇️
    \
    """)
    #создаем кнопки ответа
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    learn = types.KeyboardButton(Command.LEARN)
    stop = types.KeyboardButton(Command.STOP)
    buttons = [learn, stop]
    markup.add(*buttons)

@bot.message_handler(commands=[Command.LEARN])
def get_cards(message):

    pass

if __name__ == '__main__':
    print('Бот работает')
    bot.infinity_polling()