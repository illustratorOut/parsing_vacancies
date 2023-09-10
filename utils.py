from api import Vacancy, HHVacancy, SJVacancy


def sorting(vacancies: list[Vacancy]):
    """ Должна сортировать любой список вакансий по ежемесячной оплате"""
    return sorted(vacancies.сurrency)


def get_top(vacancies: list[Vacancy], top_count: int):
    """ Должен возвращать {top_count} записей из вакансий по зарплате"""
    return list(sorted(vacancies, reverse=True)[:top_count])


def get_currency(vacancies: list[Vacancy]):
    """ Должен возвращать список картежей пронумерованной валюты """
    count = 1
    res = []
    list_vacancies = [i.сurrency for i in vacancies]
    for i in set(list_vacancies):
        res.append({count: i})
        count += 1
    return res


def get_hh_vacancies_list(connector):
    vacancies = [
        HHVacancy(
            name=vacancy["name"],
            url=vacancy["alternate_url"],
            description=vacancy["snippet"],
            salary=vacancy["salary"]["from"] if vacancy["salary"] else None,
            сurrency=vacancy["salary"]["currency"] if vacancy["salary"] else '')
        for vacancy in connector.select({})]
    return vacancies


def get_sj_vacancies_list(connector):
    vacancies = [
        SJVacancy(
            name=vacancy["profession"],
            url=vacancy["link"],
            description=vacancy["candidat"],
            salary=vacancy["payment_from"],
            сurrency=vacancy["currency"])
        for vacancy in connector.select({})]
    return vacancies
