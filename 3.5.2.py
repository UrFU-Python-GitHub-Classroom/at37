import math
import sqlite3
import pandas as pd

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

csv_merged = pd.read_csv('../csv/vacancies_dif_currencies.csv')
print(len(csv_merged.index))

def get_avg_salary(salary_from, salary_to):
    if not math.isnan(salary_from) and not math.isnan(salary_to):
        return int((float(salary_from) + float(salary_to)) / 2)
    elif not math.isnan(salary_from):
        return int(float(salary_from))
    elif not math.isnan(salary_to):
        return int(float(salary_to))
    else:
        return None


def converter_to_rubles(value, currency, date):
    cursor = conn.execute('select * from pd_year_salary')
    names = list(map(lambda x: x[0], cursor.description))[1:]
    if currency not in names:
        return None
    else:
        cur.execute(f"SELECT {currency} FROM pd_year_salary WHERE `date` = '{date}'")
        a = cur.fetchmany()[0][0]
        if a is None:
            return None
        return int(value * a)


def rub_salary(ser):
    ser = ser.to_dict()
    salary_from, salary_to, salary_currency, date = ser['salary_from'], ser['salary_to'], ser['salary_currency'], ser['published_at'][:7]
    avg_salary = get_avg_salary(salary_to, salary_from)
    if avg_salary is not None and salary_currency is not None:
        if salary_currency == 'RUR':
            return avg_salary
        else:
            return converter_to_rubles(avg_salary, salary_currency, date)
    else:
        return None


# csv_merged['published_at'] = csv_merged['published_at'].apply(lambda x: x[:7])
csv_merged['salary'] = csv_merged.apply(rub_salary, axis=1)

csv_merged = csv_merged[['name', 'salary', 'area_name', 'published_at']]
csv_merged['published_at'] = pd.to_datetime(csv_merged['published_at'], format='%Y-%m-%dT%H:%M:%S%z')
print(csv_merged)

csv_merged.to_sql('vacancies', conn, if_exists='replace', index=False)