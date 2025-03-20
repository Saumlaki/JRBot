from src.gpt.gpt import gpt
from langchain_core.messages import HumanMessage

class QuizGPT(gpt):
    """"Класс отвечает за инициализацию GPT модели, которая может выдавать вопросы квиза.
    """
    def __init__(self):
        super().__init__("Ты ведущий программы квиз. Я прошу новый вопрос, ты даешь новый вопрос и 4 варианта ответа в формате JSON вида:"
                         "{"
                         "Вопрос: <ваш вопрос>,"
                         "Ответы:["
                         "<ответ1>,"
                         "<ответ2>,"
                         "<ответ3>,"
                         "<ответ4>"
                         "Решение: <решение>]"
                         "}")
    def set_theme(self, theme = "Общая тема"):
        self.message.append(HumanMessage(content=f"Тема игры {theme}"))
