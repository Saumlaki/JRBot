|src-корневая папка проекта
  |-ather вспомогательные классв
    |-data_session.py собирает данные сесии пользователя
    |-data_session_collector.py собирает данные сесий(data_session.py)
    |-message_templates.py вспосогательный класс который содержит определния сообщений
    |-prefix.py префиксы логических модулей
    |-word.py описывает пользовательчкое слова для модуля "Словарь"
  |-db методы работы с БД
    |-db_init.py - содержит методы загрузки, сохранения и изменения данных пользовательских словарей
  |-forms конструкторы форм
    |-inline_form.py конструктор инлайн формы
  |-gpt - гпт модели
    |-*gpt.py модель ГПТ
  |-handlers - хендлерсы
    |-*handler.py - хендлер того или иного модуля
  |-keyboards - клавиатуры
    |-*keyboard.py - клавиатура того или иного модуля
    |-keyboard_collector.py - класс агрегатор клавиатур
  |-dict_db.db - база пользовательских словарей
  |-main.py - стартовый модуль
  |-.env - настройки подключения к гигачату и к ГПТ
