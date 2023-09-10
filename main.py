import time

from connector import Connector, PathNotFoundError
from api import HH, Superjob, Vacancy, HHVacancy
from utils import get_hh_vacancies_list, get_top, sorting, get_sj_vacancies_list, get_currency


def main():
    # keyword = input("Введите ключевое слово по которому будет осуществляться поиск вакансий:\n").lower().strip()
    keyword = "python"
    hh_engine = HH(keyword)
    sj_engine = Superjob(keyword)

    hh_path_json = "hh_vacancies.json"
    sj_path_json = "sj_vacancies.json"

    hh_connector = Connector(hh_path_json)
    sj_connector = Connector(sj_path_json)

    page = 0
    hh_pages = 1
    hh_close = False
    more = True

    all_vacancy = []
    hh_all_vacancy = [0]
    sj_all_vacancy = [0]

    while not hh_close or more:
        if page < hh_pages:
            hh_engine.params["page"] = page
            page += 1
            hh_vacancies = hh_engine.get_request()
            hh_pages = hh_vacancies["pages"]
            hh_items = hh_vacancies["items"]
            hh_all_vacancy.append(len(hh_items))
            all_vacancy.append(hh_items[0])
            print(f"HH:{page}/{hh_pages}")
            hh_connector.insert(hh_items)
        else:
            hh_close = True

        if more:
            sj_engine.params["page"] = sj_engine.params["page"] + 1
            sj_vacancies = sj_engine.get_request().json()
            sj_items = sj_vacancies["objects"]
            more = sj_vacancies["more"]
            sj_all_vacancy.append(len(sj_items))
            print(f'SJ:{sj_engine.params["page"]}/{len(sj_items)}')
            sj_connector.insert(sj_items)

    print(f"HH: Найдено {sum(hh_all_vacancy)} вакансий по ключевому слову {keyword}")
    print(f"SJ: Найдено {sum(sj_all_vacancy)} вакансий по ключевому слову {keyword}")

    res_input = input("Введите команду (sort или top):\n").lower().strip()
    hh_vacancies_list = get_hh_vacancies_list(hh_connector)
    sj_vacancies_list = get_sj_vacancies_list(sj_connector)

    if res_input == "top":
        set_currency = get_currency(hh_vacancies_list)
        print("Выберите валюту:", *set_currency, sep="\n")
        currency = input()
        if currency in set_currency:
            pass

        top_n = input("Введите количество вакансий для вывода в топ N: ")
        if top_n.isdigit():
            print(*get_top(hh_vacancies_list, int(top_n)), sep="\n")
        else:
            print("Не верно введены данные: введите число")
    if res_input == "sort":
        print(*sorting(hh_vacancies_list), sep="\n")


#
# try:
#         сurrency = int(input(f"Выберите цифру валюты:\n{a}"))
#         if сurrency in a:
#             result = a[сurrency]
#         else:
#             print("Не верно указана цифра")
#
# except PathNotFoundError:
#     print(f"Дириктория {hh_path_json} не найдена.")
#     return


main()
