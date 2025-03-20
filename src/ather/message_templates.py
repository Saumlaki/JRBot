from src.ather.prefix import Prefix


class MessageTemplates:
    """"Содержит шаблоны сообщений разделенных префиксами"""
    def __init__(self):
        self.start_message = {}
        self.start_message_f = {}
        self.add_message = {}
        self.add_message_f = {}

    def get_start_message(self, prefix : str):
        return self.start_message.get(prefix)

    def add_start_message(self, prefix : str, message : str):
        self.start_message[prefix]= message

    def get_start_message_f(self, prefix : str):
        return self.start_message_f.get(prefix)

    def add_start_message_f(self, prefix : str, message : str):
        self.start_message_f[prefix]= message

    def get_add_message(self, prefix : str):
        return self.add_message.get(prefix)

    def add_add_message(self, prefix : str, message : str):
        self.add_message[prefix]= message

    def get_add_message_f(self, prefix: str):
        return self.add_message_f.get(prefix)

    def add_add_message_а(self, prefix: str, message: str):
        self.add_message_f[prefix] = message

message_templates = MessageTemplates()

#Стартовые сообщения
message_templates.add_start_message(Prefix.MAIN.value       , "Привет! Это бот для сдачи проекта по курсу *JavaRush*. Вот чем я могу быть полезен:")
message_templates.add_start_message(Prefix.RANDOM_FACT.value, "Введите название темы и я попробую удивить вас. Если тема не важна просто нажмите кнопку *Удиви меня*")
message_templates.add_start_message(Prefix.QUIZ.value       , "Введите название темы или выберете предложенную и удивите меня своими знаниями")
message_templates.add_start_message(Prefix.TALK_GPT.value   , "Всегда рад поговорить с умным человеком. Выбери тему и начнем")
message_templates.add_start_message(Prefix.TALK_FP.value    , "Сегодня мы смогли дозвонится только до этих персонажей. Выбирай и говори")
message_templates.add_start_message(Prefix.DICTIONARY.value , "Выучить пару новых слов - отличное решение. С чего начнем?")
message_templates.add_start_message(Prefix.JOB.value        , "Лучшее время для смены работы было год назад и сейчас. Давай стряхнем пыль с твоего резюме.")

#Стартовые сообщения - подвал
message_templates.add_start_message_f(Prefix.RANDOM_FACT.value, "")
message_templates.add_start_message_f(Prefix.QUIZ.value, "")
message_templates.add_start_message_f(Prefix.TALK_GPT.value, "")
message_templates.add_start_message_f(Prefix.TALK_FP.value, "")
message_templates.add_start_message_f(Prefix.DICTIONARY.value, "")
message_templates.add_start_message_f(Prefix.JOB.value, "")

#Сообщения добавления/вставки
message_templates.add_add_message(Prefix.DICTIONARY.value, "Новое слово: ")




