import math
import pandas as pd

csv_merged = pd.read_csv('vacancies_dif_currencies.csv')
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
    if currency not in df_currency.columns or df_currency[currency][date] is None or math.isnan(df_currency[currency][date]):
        # print(currency + ' ' + date + ' - проблемы')
        return None
    else:
        return int(value * df_currency[currency][date])


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

df_currency = pd.read_csv('currency_per_year.csv', index_col='date')
csv_merged['salary'] = csv_merged.apply(rub_salary, axis=1)

csv_merged[['name', 'salary', 'area_name', 'published_at']].to_csv("vacancies_preprocessed.csv", index=False)