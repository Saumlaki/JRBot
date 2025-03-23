class Word:
    def __init__(self,user_id, text, translation, show = 0, answer = 0):
        self.user_id = user_id
        self.text = text
        self.translation = translation
        self.shows = show
        self.answers = answer

