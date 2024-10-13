import random

import telebot
from telebot import types, State, custom_filters
from telebot import StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from orm_manipulation import add_words, add_user, get_words, fake_words, current_translate, delete_relation, add_word_for_user, TOKEN

state_storage = StateMemoryStorage()

# Словарь для хранения пользовательских данных
user_data = {}

API_TOKEN = TOKEN

bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage)


class Command:
    """
    Класс Команды.
    Здесь собран основной функционал бота для пользователя:
    Добавление слова для изучения, Удаление слова из изучаемых, Следующее слово, Стоп, Учиться
    """
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово 🔙'
    NEXT = 'Дальше ⏭'
    STOP = 'Ну уж нет!'
    LEARN = 'Учиться! 🇬🇧'


class MyStates(StatesGroup):
    """
    Класс созданный для обработки состояний.
    """
    target_word = State()
    translate_word = State()
    another_words = State()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    """
    Функция отправки приветственного сообщения пользователю

    :param message: команды /start или /help
    :return: текст приветственного сообщения
    """
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

@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    """
    Функция обработки команды - УДАЛИТЬ_СЛОВО
    :param message: команда УДАЛИТЬ_СЛОВО
    :return: ничего не возвращает, удаляет связь текущего пользователя со словом в таблице связей
    """
    bot.reply_to(message, "Какое слово больше учить не будем (на русском языке)?")
    user_data[message.from_user.id] = {'stage': 'RUSSIAN_WORD'}
    russian_word = user_data[message.from_user.id].get('russian_word')
    delete_relation(message.from_user.id, russian_word)
    bot.reply_to(message, f"Слово '{russian_word}' удалено для Вашего изучения.")

@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def start_add_word(message):
    """
    Функция обработки команды - ДОБАВИТЬ_СЛОВО
    :param message: команда ДОБАВИТЬ_СЛОВО
    :return: ничего не возвращает, создает связь Пользователь-Слово в таблице связей
    """
    bot.reply_to(message, "Какое слово вы хотите добавить на русском языке?")
    user_data[message.from_user.id] = {'stage': 'RUSSIAN_WORD'}

@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get('stage') == 'RUSSIAN_WORD')
def get_russian_word(message):
    """

    :param message:
    :return:
    """
    user_data[message.from_user.id]['russian_word'] = message.text
    bot.reply_to(message, "Как это слово будет на английском?")
    user_data[message.from_user.id]['stage'] = 'ENGLISH_WORD'

@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get('stage') == 'ENGLISH_WORD')
def get_english_word(message):
    """

    :param message:
    :return:
    """
    russian_word = user_data[message.from_user.id].get('russian_word')
    english_word = message.text
    #добавление в таблицу слов БД, если слова там нет
    add_words(russian_word, english_word)
    #добавление слова в таблицу связей
    add_word_for_user(message.from_user.id, russian_word)
    bot.reply_to(message, f"Слово '{russian_word}' добавлено как '{english_word}'.")

    # Удаляем данные пользователя после завершения
    del user_data[message.from_user.id]

@bot.message_handler(commands=['cancel'])
def cancel(message):
    """
    Фунция обработки команды - Отмена

    :param message: команда Отмена
    :return: сообщение, что добавление слова отменено или сообщение об отсутствии активного процесса добавления слова
    """
    if message.from_user.id in user_data:
        del user_data[message.from_user.id]
        bot.reply_to(message, "Добавление слова отменено.")
    else:
        bot.reply_to(message, "Нет активного процесса добавления слова.")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """
    Функция обработки текста.

    :param message: команды или текст
    :return: в зависимости от команды
    """
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
        word = get_words(message.from_user.id)
        if word is None:
            bot.send_message(message.chat.id, 'Похоже у Вас нет добавленных слов для обучения. Нажмите кнопку - добавить слово ➕')
        else:
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


# Обработка ответов
@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    """
    Функция обработки ответа пользователя ("Угадывание" слова).

    :param message:
    :return: сообщение пользователю, что всё правильно или что совершена ошибка
    """
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