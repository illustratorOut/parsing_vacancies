from connector import Connector, PathNotFoundError
from api import HH, Superjob, Vacancy, HHVacancy
from utils import get_hh_vacancies_list, get_top, sorting, get_sj_vacancies_list, get_currency


def main():
    count = 0
    while count == 0:
        menu = input(
            "Выберите действие:\n1.Загрузить актуальные данные с 'HH','SJ' в JSON файл\n2.Поиск вакансий (JSON файла)\n3.Завершить работу программы\n")

        hh_path_json = "hh_vacancies.json"
        sj_path_json = "sj_vacancies.json"
        hh_connector = Connector(hh_path_json)
        sj_connector = Connector(sj_path_json)
        hh_vacancies_list = get_hh_vacancies_list(hh_connector)
        sj_vacancies_list = get_sj_vacancies_list(sj_connector)

        if menu == "1":
            keyword = input("Введите ключевое слово по которому будет осуществляться поиск вакансий:\n").lower().strip()

            hh_engine = HH(keyword)
            sj_engine = Superjob(keyword)

            page = 0
            hh_pages = 1
            hh_close = False
            more = True

            all_vacancy = []
            hh_all_vacancy = [0]
            sj_all_vacancy = [0]

            while not hh_close or more:
                try:
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
                except Exception as e:
                    pass

            print(f"HH: Найдено {sum(hh_all_vacancy)} вакансий по ключевому слову {keyword}")
            print(f"SJ: Найдено {sum(sj_all_vacancy)} вакансий по ключевому слову {keyword}")

        if menu == "2":
            if hh_vacancies_list or sj_vacancies_list:

                res_input = input("Введите команду (sort или top):\n").lower().strip()

                if res_input == "top":
                    all_сurrency = set(i.сurrency for i in hh_vacancies_list + sj_vacancies_list if i.сurrency != "")

                    print("Выберите валюту:", sep="\n")
                    [print(i) for i in all_сurrency]
                    currency = input().upper().strip()
                    if currency in all_сurrency:
                        res = get_currency(hh_vacancies_list + sj_vacancies_list, currency)
                    else:
                        print("Не корректные данные, повторите попытку")
                        continue

                    top_n = input("Введите количество вакансий для вывода в топ N: ")
                    if top_n.isdigit():
                        print(*get_top(res, int(top_n)), sep="\n")
                    else:
                        print("Не корректные данные, повторите попытку")
                        continue

                elif res_input == "sort":
                    print(*sorting(hh_vacancies_list + sj_vacancies_list), sep="\n")
                else:
                    print("Не корректные данные, повторите попытку")
                    continue
            else:
                print("Файл пуст загрузите данные!")

        elif menu == "3":
            exit()


main()
