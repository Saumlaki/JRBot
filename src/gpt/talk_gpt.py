from src.gpt.gpt import gpt
from langchain_core.messages import HumanMessage

class TalkGPT(gpt):
    """"Класс отвечает за инициализацию GPT модели, которая позволит просто поболтать.
    """
    def __init__(self):
        super().__init__("Ты лучший друг и советчик давай просто поговорим")

    def set_theme(self, theme = "Общая тема"):
        pass
