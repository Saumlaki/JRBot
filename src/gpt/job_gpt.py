from src.gpt.gpt import GPT
from langchain_core.messages import HumanMessage

class TalkGPT(GPT):
    """"Класс отвечает за инициализацию GPT модели, которая поможет с составлением резюме.
    """
    def __init__(self):
        super().__init__("Помоги составить резюме на основе входящих данных")

    def set_theme(self, theme = "Общая тема"):
        pass
