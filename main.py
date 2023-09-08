from connector import Connector, PathNotFoundError
from api import HH, Superjob, Vacancy


def main():
    keyword = "python"
    hh_engine = HH(keyword)
    sj_engine = Superjob(keyword)

    hh_path_json = "hh_vacancies.json"
    sj_path_json = "sj_vacancies.json"

    try:
        hh_connector = Connector(hh_path_json)

        # Нужно подправть срез не забыть ↓↓↓ ))
        hh_connector.insert(hh_engine.get_request()['items'][:10])

        list_vacancy = [
            Vacancy(i['name'], i['alternate_url'], i["salary"]["from"], i["snippet"]["responsibility"],
                    i["salary"]["currency"]) for i in hh_engine.get_request()['items'] if
            i["salary"] is not None and i["salary"].get("from", 0)]

        # print(list_vacancy)
        print(hh_connector.select())


    except PathNotFoundError:
        print(f"Дириктория {hh_path_json} не найдена.")
        return





    # sj_connector = Connector(sj_path)
    # page = 0
    # hh_pages = 1
    # hh_close = False
    # more = True

    # while not hh_close and more:
    #     if page < hh_pages:
    #         hh_engine.params["page"] = page
    #         page += 1
    #         hh_vacancies = hh_engine.get_request().json
    #         hh_pages = hh_vacancies["pages"]
    #         hh_items = hh_vacancies["items"]
    #         hh_connector.insert(hh_items)
    #     else:
    #         hh_close = True
    #
    #     if more:
    #         sj_engine.params["page"] = sj_engine.params["page"] + 1
    #         sj_vacancies = sj_engine.get_requests().json()
    #         sj_items = sj_vacancies["objects"]
    #         more = sj_vacancies["more"]
    #         sj_connector.insert(sj_items)
    #


main()
