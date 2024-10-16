import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

"""
Описание модели хранения данных в БД бота
"""

Base = declarative_base()

class Words(Base):
    __tablename__ = 'tg_words'

    id = sq.Column(sq.Integer, primary_key=True)
    russian_word = sq.Column(sq.String(length=100), unique=True)
    current_english_word = sq.Column(sq.String(length=100), unique=True)

class Users(Base):
    __tablename__ = 'tg_users'

    id = sq.Column(sq.Integer, primary_key=True)

class WordsForUsers(Base):
    __tablename__ = 'tg_words_for_users'

    id_relations = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('tg_users.id'), nullable=False)
    word_id = sq.Column(sq.Integer, sq.ForeignKey('tg_words.id'), nullable=False)


class Facts(Base):
    __tablename__ = 'tg_facts'

    id_operation = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('tg_users.id'), nullable=False)
    word_id = sq.Column(sq.Integer, sq.ForeignKey('tg_words.id'), nullable=False)
    answer = sq.Column(sq.String(length=100), nullable=False)
    date_time = sq.Column(sq.DateTime, nullable=False)

    words = relationship(Words, backref='tg_facts')
    users = relationship(Users, backref='users')


def create_tables(engine):
    Base.metadata.create_all(engine)