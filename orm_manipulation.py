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

    pass

def get_words():
    session.query(Words.russian_word).select_from(Words).get(1)

def current_translate(message):
    res = session.query(Words.current_english_word).select_from(Words).filter(Words.russian_word == message).all()
    return res

def fake_words(message):
    res = session.query(Words.current_english_word).select_from(Words).filter(Words.russian_word != message).all()
    return res

if __name__ == '__main__':
    get_words()