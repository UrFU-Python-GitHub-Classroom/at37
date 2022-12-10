import pandas as pd

df = pd.read_csv('vacancies_by_year.csv')

df['years'] = df['published_at'].apply(lambda x: int(x[:4]))  # 650 ms

df_grup = df.groupby(['years'])

for key, value in df_grup:
    print(key)
    value[['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']].to_csv(f"Seperated csv/chunk_{key}.csv", index=False)