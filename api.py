"""Создать абстрактный класс для работы с API сайтов с вакансиями.
Реализовать классы, наследующиеся от абстрактного класса, для работы с конкретными платформами.
Классы должны уметь подключаться к API и получать вакансии."""
import os
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
        return requests.get(self.url, params=self.params).json()


class Superjob(ConnectionApi):
    def __init__(self, keyword, page=1):
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.params = {
            "keywords[0][keys]": keyword,
            "keywords[0][sews]": 4,
            "keywords[0][skwc]": "or",
            "page": page,
            "count": 100,
        }

    def get_request(self):
        headers = {"X-Api-App-Id": os.environ["SUPERJOB_API_KEY"]}
        return requests.get(self.url, headers=headers, params=self.params)


class Vacancy:
    def __init__(self, name, url, salary, description, сurrency):
        self.name = name
        self.url = url
        self.salary = salary
        self.description = description
        self.сurrency = сurrency

    def __lt__(self, other):
        """Для оператора меньше <"""
        pass

    def __gt__(self, other):
        """Для оператора больше >"""
        return self.salary > other.salary

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', url='{self.url}', salary='{self.salary}', description='{self.description}, сurrency='{self.сurrency}')"


class HHVacancy(Vacancy):

    def __str__(self):
        return f'HH: {self.name}, зарплата: {self.salary} руб/мес'
