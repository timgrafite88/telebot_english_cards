import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from orm_manipulation import add_words, add_user, get_words, fake_words, current_translate

API_TOKEN = '<YOUR_TOKEN>'

bot = telebot.TeleBot(API_TOKEN)

class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово 🔙'
    NEXT = 'Дальше ⏭'
    STOP = 'Ну уж нет!'
    LEARN = 'Учиться! 🇬🇧'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    # создаем кнопки ответа
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    learn = types.KeyboardButton(Command.LEARN)
    stop = types.KeyboardButton(Command.STOP)
    markup.add(learn, stop)
    bot.send_message(message.chat.id, f"""\
    Привет, {message.from_user.first_name} 👋 
    Давай попрактикуемся в английском языке. Тренировки можешь проходить в удобном для себя темпе.
    У тебя есть возможность использовать тренажёр, как конструктор, и собирать свою собственную базу для обучения. Для этого воспрользуйся инструментами:
    добавить слово ➕,
    удалить слово 🔙.
    Ну что, начнём ⬇️
    \
    """, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == Command.LEARN:
        #если учимся - создаем кнопки после ответа
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        add_btn = types.KeyboardButton(Command.ADD_WORD)
        delete_btn = types.KeyboardButton(Command.DELETE_WORD)
        next_btn = types.KeyboardButton(Command.NEXT)
        markup.add(add_btn, delete_btn, next_btn)
        bot.send_message(message.chat.id,'Отлично! Удачи в обучении!', reply_markup=markup)

    elif message.text == Command.STOP:
        bot.send_message(message.chat.id, 'Жаль! Учиться - это здорово!')

    elif message.text == Command.NEXT:
        word = get_words()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        bot.send_message(message.chat.id, f'Отгадай слово {word}!', reply_markup=markup)

    elif message.text == Command.ADD_WORD:
        pass

    elif message.text == Command.DELETE_WORD:
        pass

if __name__ == '__main__':
    print('Бот работает')
    bot.infinity_polling()