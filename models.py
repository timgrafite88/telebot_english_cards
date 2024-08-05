import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Words(Base):
    __tablename__ = 'words'

    id = sq.Column(sq.Integer, primary_key=True)
    russian_word = sq.Column(sq.String(length=100), unique=True)
    current_english_word = sq.Column(sq.String(length=100), unique=True)
    fake_english_translate_one = sq.Column(sq.String(length=100), nullable=False)
    fake_english_translate_two = sq.Column(sq.String(length=100), nullable=False)
    fake_english_translate_three = sq.Column(sq.String(length=100), nullable=False)