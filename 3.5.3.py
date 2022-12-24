import sqlite3
import pandas as pd

vac_name = 'Программист'
conn = sqlite3.connect('db.sqlite3')

df_years_salary_dic = pd.read_sql(f"SELECT ROUND(AVG(salary)), strftime('%Y', published_at) \
                                    FROM vacancies \
                                    GROUP BY strftime('%Y', published_at)", conn)
df_years_salary_dic.to_csv('df_years_salary_dic.csv', index=False)

df_years_count_dic = pd.read_sql(f"SELECT COUNT(*), strftime('%Y', published_at) \
                                    FROM vacancies \
                                    GROUP BY strftime('%Y', published_at)", conn)
df_years_count_dic.to_csv('df_years_count_dic.csv', index=False)

df_years_salary_vac_dic = pd.read_sql(f"SELECT ROUND(AVG(salary)), strftime('%Y', published_at) \
                                        FROM vacancies  \
                                        WHERE name like '%{vac_name}%' \
                                        GROUP BY strftime('%Y', published_at)", conn)
df_years_salary_vac_dic.to_csv('df_years_salary_vac_dic.csv', index=False)

df_years_count_vac_dic = pd.read_sql(f"SELECT COUNT(salary), strftime('%Y', published_at) \
                                       FROM vacancies \
                                       WHERE name like '%{vac_name}%' \
                                       GROUP BY strftime('%Y', published_at)", conn)
df_years_count_vac_dic.to_csv('df_years_count_vac_dic.csv', index=False)

df_area_salary_dic = pd.read_sql(f"SELECT ROUND(AVG(salary)), area_name \
                                   FROM vacancies \
                                   GROUP BY area_name \
                                   HAVING COUNT(salary) > (\
                                       SELECT COUNT(salary) \
                                       FROM vacancies \
                                   ) / 100 \
                                   ORDER BY ROUND(AVG(salary)) DESC \
                                   LIMIT 10", conn)
df_area_salary_dic.to_csv('df_area_salary_dic.csv', index=False)

df_area_count_dic = pd.read_sql(f"SELECT ROUND(COUNT(salary) * 1.0 / ( \
                                      SELECT COUNT(salary) FROM vacancies), 4 \
                                  ), area_name \
                                  FROM vacancies \
                                  GROUP BY area_name \
                                  ORDER BY COUNT(salary) DESC \
                                  LIMIT 10", conn)
df_area_count_dic.to_csv('df_area_count_dic.csv', index=False)