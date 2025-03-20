import enum

class Prefix(enum.Enum):
    """Задает префиксы для сообщений модулей"""
    MAIN        = "main_"
    RANDOM_FACT = "r_fact_"
    QUIZ        = "quiz_"
    DICTIONARY  = "dict_"
    TALK_GPT    = "tgpt_"
    TALK_FP     = "tfp_"
    JOB         = "job_"