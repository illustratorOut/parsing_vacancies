import json
import os


class PathNotFoundError(Exception):
    pass


class Connector:
    """Работа с JSON файлом (информации о вакансиях в файл)"""

    def __init__(self, file_path):
        self.__data_file = file_path
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """Проверяет на существование файла и создает его в случае необходимости """
        try:
            if not os.path.exists(self.__data_file):
                with open(self.__data_file, 'w') as file:
                    file.write(json.dumps([]))
        except FileNotFoundError:
            raise PathNotFoundError

    def insert(self, data):
        """Запись данных в файл с сохранением структуры и исходных данных"""
        with open(self.__data_file, 'r') as file:
            file_data = json.load(file)
        with open(self.__data_file, 'w') as file:
            json.dump(file_data + data, file, indent=4, ensure_ascii=False)

    def select(self, query):
        """Выбор данных из файла с применением фильтрации query содержит словарь"""
        with open(self.__data_file, 'r') as file:
            file_data = json.load(file)

        if not query:
            return file_data

        res = []
        for item in file_data:
            if item['price'] >= query:
                res.append(item)
        return res
