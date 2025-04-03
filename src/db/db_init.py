import sqlite3
import json

from src.ather.word import Word
from src.gpt.gpt import GPT


def init_db():
    result = False

    connection = sqlite3.connect('dict_db.db')
    cursor = connection.cursor()
    # Создаем таблицу dictionary
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dictionary (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        text TEXT,
        translation TEXT,
        shows INTEGER,
        answers INTEGER
        username TEXT NOT NULL)''')
    connection.commit()
    connection.close()


def load_dictionary(id_session):
    dictionary = []
    connection = sqlite3.connect('dict_db.db')
    cursor = connection.cursor()

    cursor.execute(f'SELECT text, translation, shows, answers FROM dictionary WHERE user_id = {id_session}')
    words = cursor.fetchall()

    # Выводим результаты
    for word in words:
        dictionary.append(Word(id_session, word[0],word[1],word[2],word[3]))
    return dictionary


def save_word(word: Word):
    connection = sqlite3.connect('dict_db.db')
    cursor = connection.cursor()

    cursor.execute(f' INSERT INTO dictionary (user_id, text, translation, shows, answers) '
                   f' SELECT {word.user_id}, \'{word.text}\', \'{word.translation}\', {word.shows}, {word.answers}'
                   f' WHERE NOT EXISTS ('
                   f' SELECT 1 FROM dictionary WHERE user_id = {word.user_id} AND text = \'{word.text}\''
                   f')')
    connection.commit()
    connection.close()

def update_word(word: Word):
    connection = sqlite3.connect('dict_db.db')
    cursor = connection.cursor()

    cursor.execute(f' UPDATE dictionary'
                   f' SET   shows = \'{word.shows}\', '
                   f'       answers = \'{word.answers}\' '
                   f' WHERE user_id = {word.user_id} AND text = {word.text}')
    connection.commit()
    connection.close()
