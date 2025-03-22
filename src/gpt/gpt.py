from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

from src.config_reader import  config


class GPT:
    def __init__(self, behavior : str):
        self.giga = GigaChat(credentials=config.credentials.get_secret_value(), verify_ssl_certs = False)
        self.message = [SystemMessage(content=behavior)]

    def get_answer(self, content : str):

        self.message.append(HumanMessage(content=content))
        res = self.giga.invoke(self.message)
        self.message.append(res)
        return res.content