import pandas as pd
import requests
import concurrent.futures
from datetime import datetime, timedelta


def serialization(vacancy):
    return {
        'name': vacancy['name'],
        'salary_from': vacancy['salary']['from'] if vacancy['salary'] else None,
        'salary_to': vacancy['salary']['to'] if vacancy['salary'] else None,
        'salary_currency': vacancy['salary']['currency'] if vacancy['salary'] else None,
        'area_name': vacancy['area']['name'] if vacancy['area'] else None,
        'published_at': vacancy['published_at'],
    }


def get_chunk(url_request):
    resp = requests.get(url_request)
    resp_json = resp.json()
    if resp.status_code != 200:
        print(resp_json)
        if "errors" in resp_json and any(["value" in error and error["value"] == "captcha_required" for error in resp_json["errors"]]):
            print('Капча')
            return
        else:
            print(url_request)
            return get_chunk(url_request)
    vacancies = resp_json["items"]
    return [pd.Series(serialization(vac)).to_frame().T for vac in vacancies]


if __name__ == '__main__':
    detes_hours = pd.period_range(
        datetime.now() - timedelta(days=1, hours=1),
        datetime.now() - timedelta(hours=1),
        freq="H"
    ).strftime('%Y-%m-%dT%H:00:00').tolist()
    print(detes_hours)
    print(len(detes_hours))

    requests_list = []
    for i in range(len(detes_hours) - 1):
        for chunk_number in range(0, 20):
            requests_list.append(f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={chunk_number}&date_from={detes_hours[i]}&date_to={detes_hours[i + 1]}')

    # print(requests_list)
    print(len(requests_list))

    vacancies = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        csv_string = [executor.submit(get_chunk, url_request) for url_request in requests_list]
        for future in concurrent.futures.as_completed(csv_string):
            vacancies += future.result()

    df = pd.concat(vacancies, ignore_index=True)
    df.to_csv('vacancies.csv', index=False)
    print(df)