from src.gpt.gpt import gpt
from langchain_core.messages import HumanMessage

class TalkGPT(gpt):
    """"Класс отвечает за инициализацию GPT модели, которая поможет с составлением резюме.
    """
    def __init__(self):
        super().__init__("Помоги составить резюме на основе входящих данных")

    def set_theme(self, theme = "Общая тема"):
        pass
