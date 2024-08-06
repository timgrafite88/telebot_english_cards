import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

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
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    learn = types.KeyboardButton(Command.LEARN)
    stop = types.KeyboardButton(Command.STOP)
    buttons = [learn, stop]
    markup.add(*buttons)




if __name__ == '__main__':
    print('Бот работает')
    bot.infinity_polling()