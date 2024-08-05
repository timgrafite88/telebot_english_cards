import telebot
from telebot import types

API_TOKEN = '<YOUR_TOKEN>'

bot = telebot.TeleBot(API_TOKEN)

class Buttons:
    delete_word = 'Удалить слово 🔙'
    add_word = 'Добавить слово ➕'

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

@bot.message_handler(commands=['start', 'cards'])
def get_cards(message):


if __name__ == '__main__':
    print('Бот работает')
    bot.infinity_polling()