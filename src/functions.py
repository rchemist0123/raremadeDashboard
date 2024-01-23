import sqlite3
import pandas as pd


def fetch_daily_data():
    conn = sqlite3.connect(database='raremade.db')
    data = pd.read_sql_query("""
                SELECT
                    dates,
                    sum(case when category1 = '수입' then price else 0 end) as income,
                    sum(case when category1 = '지출' and unit = '위안' then price * 180
                             when category1 = '지출' and unit = '원' then price else 0 end) as expenditure,
                    sum(case when category1 = '수입' then price else 0 end) - 
                        sum(case when category1 = '지출' and unit = '위안' then price * 180
                        when category1 = '지출' and unit = '원' then price else 0 end) as daily_revenue
                FROM data
                GROUP BY dates
                ORDER BY dates desc
            """, conn)
    conn.close()
    return data

def fetch_all_data():
    conn = sqlite3.connect(database='raremade.db')
    data = pd.read_sql_query("""
                            SELECT dates, category1, category2, category3, price, unit, 
                             case when unit = '위안' then price * 180 else price end as price_final
                            FROM data order by dates desc
                             """, conn)
    conn.close()
    return data