
class DataSession:
    """"Хранит данные сессии пользователя
    """
    def __init__(self, id_session:int):
        self.id_session = id_session

        self.quiz_questions = ""
        self.quiz_answers = ""
        self.quiz_results = 0
        self.quiz_count = 0
        self.quiz_theme = ""

        self.random_fact_num= 0 # Количество узнанных новых фактов

        self.dictionary_learn_now= {} # Содержит словарь слов в текущей сессии к изучению
        self.dictionary_learn_all= {} # Содержит словарь слов к изучению

        self.gpt = None

        self.msg_talk_gpt = None