import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models import create_tables, Users, Facts, Words, WordsForUsers
import random
import configparser

# создаём объекта парсера
config = configparser.ConfigParser()
# читаем конфиг
config.read("settings.ini")

# получаем токен бота
TOKEN = config["TOKENS"]["bot_token"]

user = config["DATABASE"]["user"]
password = config["DATABASE"]["password"]
localhost = config["DATABASE"]["localhost"]
db_name = config["DATABASE"]["db_name"]

# подключение к базе PostgreSQL
DSN = f'postgresql://{user}:{password}@localhost:{localhost}/{db_name}'

engine = sqlalchemy.create_engine(DSN)

# #создание объектов
#create_tables(engine)

Session = sessionmaker(bind=engine)

def add_words(russian_word, current_english_word):
    """Функция добавления слова в таблицу слов

        Входные параметры:
        russian_word: слово на русском языке
        current_english_word: корректный перевод на английский язык

    """
    with Session() as session:
        existing_word = session.query(Words).filter_by(russian_word=russian_word).first()
        if existing_word:
            return
        new_word = Words(russian_word=russian_word, current_english_word=current_english_word)
        session.add(new_word)
        session.commit()


def add_word_for_user(user, russian_word):
    """Функция добавления слова в для конкректного пользователя.
        Формирования связи Пользователь-Слово.

        Входные параметры:
        user: id пользователя
        russian_word: слово на русском языке, которое добавляется к изучению
        """
    with Session() as session:
        rw = session.query(Words.id).select_from(Words).filter(Words.russian_word == russian_word).first()
        id_word = rw[0]
        relation = WordsForUsers(user_id=user, word_id=id_word)
        session.add(relation)
        session.commit()

def add_user(message):
    """Функция добавления пользователя в БД бота"""
    with Session() as session:
        user_ids = session.query(Users.id).select_from(Users).all()
        if not user_ids or message not in [user[0] for user in user_ids]:
            new_user = Users(id=message)
            session.add(new_user)
            session.commit()

def delete_relation(user_id, russian_word):
    """
    Функция удаления связи Пользователь-Слово, когда мы убираем слово из изучаемых.

    :param user_id: id пользователя
    :param russian_word: слово на русском языке
    :return: ничего не возвращае, происходит удаление связи
    """
    with Session() as session:
        rw = session.query(Words.id).select_from(Words).filter(Words.russian_word == russian_word).first()
        id_word = rw[0]
        dw = session.query(WordsForUsers).filter(WordsForUsers.user_id == user_id and WordsForUsers.word_id == id_word).first()
        session.delete(dw)
        session.commit()

#Функция получения рандомного слова на русском для перевода
def get_words(user_id):
    """
    Функция выдачи слова пользователю для угадывания перевода.

    :param user_id: id пользователя
    :return: рандомное слово на русском языке из изучаемых пользователем (слова у которых имеется связь с текущим пользователем)
    """
    with Session() as session:
        wrds = session.query(WordsForUsers.word_id).select_from(WordsForUsers).filter(
            WordsForUsers.user_id == user_id).all()
        words_id_list = list(set([w[0] for w in wrds]))
        word_id = random.choice(words_id_list)
        res = session.query(Words.russian_word).select_from(Words).filter(Words.id == word_id).first()
        return res[0]

#Функция получения корректного анлийского слова
def current_translate(message):
    """
    Функция возврата корректного перевода на английский язык текущего "угадываемого" слов на русском.

    :param message: слово на русском языке
    :return: слово корректного перевода на английский
    """
    with Session() as session:
        res = session.query(Words.current_english_word).select_from(Words).filter(Words.russian_word == message).all()
        return res[0][0]

#Функция для получения слов с неправильным переводом для кнопок выбора
def fake_words(message):
    """
    Функция возврата альтернативных вариантов для перевода.

    :param message: слово на русском языке
    :return: список из 3-х альтернативных вариантов
    """
    with Session() as session:
        res = session.query(Words.current_english_word).select_from(Words).filter(Words.russian_word != message).all()
        words = [w[0] for w in res]
        random.shuffle(words)
        return words[:3]

# if __name__ == '__main__':