from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat


class gpt:
    def __init__(self, behavior : str):
        self.giga = GigaChat(credentials="ххххххххх", verify_ssl_certs = False)
        self.message = [SystemMessage(content=behavior)]

    def get_answer(self, content : str):

        self.message.append(HumanMessage(content=content))
        res = self.giga.invoke(self.message)
        self.message.append(res)
        return res.content