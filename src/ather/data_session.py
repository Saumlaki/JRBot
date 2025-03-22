class DataSession:
    """"Хранит данные сессии пользователя
    """

    def __init__(self, id_session: int):
        self.id_session = id_session

        self.clear()

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

        self.dictionary_learn_now = {}  # Содержит словарь слов в текущей сессии к изучению
        self.dictionary_learn_all = {}  # Содержит словарь слов к изучению
