from src.gpt.gpt import gpt
from langchain_core.messages import HumanMessage

class RandomFactGPT(gpt):
    """"Класс отвечает за инициализацию GPT модели, которая может выдавать случайные факты.
    """
    def __init__(self):
        super().__init__("Ты знаешь много интересных фактов. Я говорю Следующий, ты говоришь мне новый факт на указанную ранее тему. "
                         "Если факта нет то пришли пустую строку")

    def set_theme(self, theme = "Любые факты"):
        self.message.append(HumanMessage(content=f"Тема интересных фактов {theme}"))
