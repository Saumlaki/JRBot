import sqlite3
import json

from src.gpt.gpt import GPT


def init_db():

    result = False

    connection = sqlite3.connect('dict_db.db')
    cursor = connection.cursor()
    # Создаем таблицу Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL)''')

    # Создаем таблицу топ 500 слов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Top500 (
        id INTEGER PRIMARY KEY,
        word TEXT NOT NULL,
        translation TEXT NOT NULL)''')

    # Создаем таблицу выученных слов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dictionary (
        id INTEGER PRIMARY KEY,
        user_id_ INTEGER NOT NULL,
        world_id INTEGER NOT NULL,
        status INTEGER NOT NULL,
        show INTEGER NOT NULL,
        repeat INTEGER NOT NULL,
        word TEXT NOT NULL,
        translation TEXT NOT NULL)''')

    gpt = GPT("Ты даешь только ответы на вопросы без своих комментариев.")
    answer_json = gpt.get_answer("верни весь ответ в формате JSON. Топ 10 английских слов")

    answer_json = answer_json.replace("json","")
    answer_json = answer_json.replace("`","")
    print(answer_json)
    answer_dict = json.loads(answer_json)

    if "top_ten_english_words" in answer_dict.keys():
        for world in answer_dict["top_ten_english_words"]:

            translate = gpt.get_answer(f"Верни только перевод слова {world}")
            cursor.execute(f'INSERT INTO Top500 (word, translation) VALUES ({world}, {translate})')
            connection.commit()
    if "top_ten_words" in answer_dict.keys():
        for world in answer_dict["top_ten_english_words"]:

            translate = gpt.get_answer(f"Верни только одно значение перевода слова {world}")
            cursor.execute(f'INSERT INTO Top500 (word, translation) VALUES ({world}, {translate})')
            connection.commit()
    connection.commit()
    connection.close()






# # Сохраняем изменения и закрываем соединение
# connection.commit()
# connection.close()
#
#
# connection = sqlite3.connect('my_database.db')
# cursor = connection.cursor()
#
# # Добавляем нового пользователя
# cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', ('newuser', 'newuser@example.com', 28))
#
# # Сохраняем изменения и закрываем соединение
# connection.commit()
# connection.close()
#
# # Устанавливаем соединение с базой данных
# connection = sqlite3.connect('my_database.db')
# cursor = connection.cursor()
#
# # Обновляем возраст пользователя "newuser"
# cursor.execute('UPDATE Users SET age = ? WHERE username = ?', (29, 'newuser'))
#
# # Сохраняем изменения и закрываем соединение
# connection.commit()
# connection.close()
#
#
# # Устанавливаем соединение с базой данных
# connection = sqlite3.connect('my_database.db')
# cursor = connection.cursor()
#
# # Выбираем всех пользователей
# cursor.execute('SELECT * FROM Users')
# users = cursor.fetchall()
#
# # Выводим результаты
# for user in users:
#   print(user)
#
# # Закрываем соединение
# connection.close()