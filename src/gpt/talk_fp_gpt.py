from src.gpt.gpt import GPT
from langchain_core.messages import HumanMessage

class TalkGPT(gpt):
    """"Класс отвечает за инициализацию GPT модели, которая позволит поговорить с известной личностью
    """
    def __init__(self):
        super().__init__("Ты говоришь от лица другого персонажа")

    def set_theme(self, theme = "Общая тема"):
        pass
