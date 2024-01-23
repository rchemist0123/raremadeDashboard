from dash import dcc, State, Input, Output, callback
import sqlite3
from functions import fetch_all_data, fetch_daily_data

@callback(
    Output("download_csv", 'data'),
    Input('btn_csv', 'n_clicks'),
    prevent_initial_call = True,
    suppress_callback_exceptions = True
)
def download(n_clicks):
    return dcc.send_data_frame(fetch_all_data().to_csv, 'All_data.csv')

@callback(
    Output('category2','options'),
    Input('category1', 'value')
)
def set_category_detail(value):
    if value == '수입':
        return [{'label':i, 'value':i} for i in ['스마트스토어','도매','기타']]
    elif value == '지출':
        return [{'label':i, 'value':i} for i in ['물품 구입','광고비','세금', '기타']]
    return []

@callback(
    Output('price_transform', 'children'),
    Input('price', 'value'),
    Input('price_unit', 'value')
)
def transform_price(price:int, unit):
    if unit == '위안':
        price_new = price * 180
        return "{:,} {}".format(price_new,'원')


@callback(
    # Output('table','data'), 
    Output('daily_table','data'),
    Input('submit','n_clicks'),
    State("date",'date'),
    State("category1", 'value'),
    State("category2", 'value'),
    State("category3", 'value'),
    State("price", 'value'),
    State("price_unit",'value')
)
def insert_record(n_clicks, date, cat1, cat2, cat3, price, unit):
    if n_clicks > 0:
        conn = sqlite3.connect('raremade.db')
        cursor = conn.cursor()
        cursor.execute("insert into data (dates, category1, category2, category3, price, unit) values (?,?,?,?,?,?)", 
                       (date, cat1, cat2, cat3, price, unit))
        conn.commit()
        conn.close()
        
    return fetch_daily_data().to_dict('records')
