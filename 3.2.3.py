import concurrent.futures
import os
import pandas as pd
import time

file_name = 'vacancies_by_year.csv'
vac_name = 'Программист'


def chunk_processing(file):
    df = pd.read_csv(file)
    df['published_at'] = df['published_at'].apply(lambda x: int(x[:4]))  # 650 ms
    df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
    year = df['published_at'][0]

    df_this_profession = df[df['name'].str.contains(vac_name)]

    years_salary = (year, int(df[df['published_at'] == year]['salary'].mean()))
    years_count = (year, len(df[df['published_at'] == year].index))

    years_salary_vac = (year, int(df_this_profession[df_this_profession['published_at'] == year]['salary'].mean()))
    years_count_vac = (year, len(df_this_profession[df_this_profession['published_at'] == year].index))

    return years_salary, years_count, years_salary_vac, years_count_vac


if __name__ == '__main__':
    start_time = time.time()

    path = 'Separated csv/'
    file_list = [path + f for f in os.listdir(path) if f.endswith('.csv')]

    stat_list = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        future_to_url = [executor.submit(chunk_processing, file) for file in file_list]
        for future in concurrent.futures.as_completed(future_to_url):
            stat_list.append(future.result())

    years_salary_dic = {stat[0][0]: stat[0][1] for stat in stat_list}
    years_count_dic = {stat[1][0]: stat[1][1] for stat in stat_list}
    years_salary_vac_dic = {stat[2][0]: stat[2][1] for stat in stat_list}
    years_count_vac_dic = {stat[3][0]: stat[3][1] for stat in stat_list}

    print("Динамика уровня зарплат по годам: " + str(years_salary_dic))
    print("Динамика количества вакансий по годам: " + str(years_count_dic))
    print("Динамика уровня зарплат по годам для выбранной профессии: " + str(years_salary_vac_dic))
    print("Динамика количества вакансий по годам для выбранной профессии: " + str(years_count_vac_dic))

    print(f"--- {(time.time() - start_time)} seconds ---")