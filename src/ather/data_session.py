from src.db import db_init


class DataSession:
    """"Хранит данные сессии пользователя
    """

    def __init__(self, id_session: int):
        self.id_session = id_session

        self.clear()
        self.load_dictionary(self.id_session)

    def get_empty_job(self):
        return {"name": "", "prof": "", "salary": "0"}

    def clear(self):
        self.msg_talk_gpt = None
        self.gpt = None

        self.random_fact_num = 0  # Количество узнанных новых фактов

        self.quiz_results = 0  # Количество правильных ответов
        self.quiz_count = 0  # Количество заданных вопросов
        self.quiz_answers = ""  # Правильный ответ на вопрос квиза
        self.job = self.get_empty_job()  # формирует пустую структуру резюме

        self.current_word = None

    def load_dictionary(self, id_session):
        self.dictionary = db_init.load_dictionary(id_session)

    def save_dictionary_word(self, word):
        db_init.save_word(word)

    def update_word(self, word):
        db_init.update_word(word)
