import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models import create_tables, Users, Facts, Words
import random

# подключение к базе PostgreSQL
DSN = 'postgresql://postgres:123@localhost:5432/my_music_site'

engine = sqlalchemy.create_engine(DSN)

# #создание объектов
#create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_words(message):

    pass

def add_user(message):
    user_ids = session.query(Users.id).select_from(Users).all()
    if not user_ids or message not in [user[0] for user in user_ids]:
        new_user = Users(id=message)
        session.add(new_user)
        session.commit()

#Функция получения рандомного слова на русском для перевода
def get_words():
    res = session.query(Words.russian_word).select_from(Words).all()
    words = [w[0] for w in res]
    word = random.choice(words)
    return word


#Функция получения корректного анлийского слова
def current_translate(message):
    res = session.query(Words.current_english_word).select_from(Words).filter(Words.russian_word == message).all()
    return res[0][0]

#Функция для получения слов с неправильным переводом для кнопок выбора
def fake_words(message):
    res = session.query(Words.current_english_word).select_from(Words).filter(Words.russian_word != message).all()
    words = [w[0] for w in res]
    random.shuffle(words)
    return words[:3]

# if __name__ == '__main__':
#     add_user(11)
#     translate = current_translate('Стол')
#     print(translate)
    # others = get_words()
    # print(others)

