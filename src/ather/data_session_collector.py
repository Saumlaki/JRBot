from src.ather.data_session import DataSession


class DataSessionCollector:

    def __init__(self):
        self.data_helper_dict = {}

    def get_data_session(self, id_session:int):
        if id_session in self.data_helper_dict:
            return self.data_helper_dict[id_session]
        else:
            data_helper = DataSession(id_session)
            self.data_helper_dict[id_session] = data_helper
            return data_helper