from src.gpt.gpt import GPT
from langchain_core.messages import HumanMessage

class DictionaryGPT(GPT):
    """"Класс отвечает за инициализацию GPT модели, которая поможет с составлением резюме.
    """
    def __init__(self):
        super().__init__("Ты помогаешь учить слова по английскому языку")

    def set_theme(self, theme = "Общая тема"):
        pass
