"""Создать абстрактный класс для работы с API сайтов с вакансиями.
Реализовать классы, наследующиеся от абстрактного класса, для работы с конкретными платформами.
Классы должны уметь подключаться к API и получать вакансии."""

from abc import ABC, abstractmethod

import requests


class ConnectionApi(ABC):

    @abstractmethod
    def get_request(self):
        pass


class HH(ConnectionApi):
    params = {
        "found": 1,
        "per_page": 100,
        "pages": 1,
        "page": 0,
        "items": [{}]
    }

    def __init__(self, word, page=0):
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            'text': word,
            'page': page,
            'per_page': 100,
            'search_field': 'name'
        }

    def get_request(self):
        res = requests.get(self.url, params=self.params).json()
        print(res)


a = HH('Python')
a.get_request()


class Vacancy:
    def __init__(self, name, url, salary, description):
        self.name = name
        self.url = url
        self.salary = salary
        self.description = description

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        return self.salary > other.salary

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', url='{self.url}', salary='{self.salary}', description='{self.description}')"


class HHVacancy(Vacancy):

    def __str__(self):
        return f'HH: {self.name}, зарплата: {self.salary} руб/мес'
