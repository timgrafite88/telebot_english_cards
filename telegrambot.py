import random

import telebot
from telebot import types, State, custom_filters
from telebot import StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from orm_manipulation import add_words, add_user, get_words, fake_words, current_translate

state_storage = StateMemoryStorage()

API_TOKEN = '7136253038:AAEYeQoigoiQfIyLDRbDTg1_MAqdC7YH2gk'

bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage)


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово 🔙'
    NEXT = 'Дальше ⏭'
    STOP = 'Ну уж нет!'
    LEARN = 'Учиться! 🇬🇧'


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


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

        add_user(message.from_user.id)
        #если учимся - создаем кнопки после ответа
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        add_btn = types.KeyboardButton(Command.ADD_WORD)
        delete_btn = types.KeyboardButton(Command.DELETE_WORD)
        next_btn = types.KeyboardButton(Command.NEXT)
        markup.add(add_btn, delete_btn, next_btn)
        bot.send_message(message.chat.id, 'Отлично! Удачи в обучении!', reply_markup=markup)

    elif message.text == Command.STOP:
        bot.send_message(message.chat.id, 'Жаль! Учиться - это здорово!')

    elif message.text == Command.NEXT:
        word = get_words()
        eng_translate = current_translate(word)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        # Создаем кнопки
        btm1 = types.KeyboardButton(eng_translate)
        fake_btms = fake_words(word)
        other = [types.KeyboardButton(w) for w in fake_btms]

        buttons = [btm1] + other
        random.shuffle(buttons)
        # Добавляем кнопки в список

        add_btn = types.KeyboardButton(Command.ADD_WORD)
        delete_btn = types.KeyboardButton(Command.DELETE_WORD)
        next_btn = types.KeyboardButton(Command.NEXT)
        buttons.extend([add_btn, delete_btn, next_btn])
        markup.add(*buttons)

        bot.send_message(message.chat.id, f'Отгадай слово {word}!', reply_markup=markup)

        bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['target_word'] = word
            data['translate_word'] = eng_translate
            data['other_words'] = fake_btms

    elif message.text == Command.ADD_WORD:
        pass

    elif message.text == Command.DELETE_WORD:
        pass

@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if 'target_word' in data:
            word = data['target_word']
            if message.text == word:
                bot.send_message(message.chat.id, 'Всё правильно!')
            else:
                bot.send_message(message.chat.id, 'Ошибка!')


if __name__ == '__main__':
    print('Бот работает')
    bot.infinity_polling()