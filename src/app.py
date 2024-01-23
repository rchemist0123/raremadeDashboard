from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
from dash.dash_table.Format import Format, Group
import pandas as pd
from datetime import date
import sqlite3

columns_daily = [
    dict(id="dates", name="일자"),
    dict(id="income", name="수입", type = "numeric", format = Format().group(True)),
    dict(id="expenditure", name="지출",  type = "numeric", format = Format().group(True)),
    dict(id="daily_revenue", name="일일정산",  type = "numeric", format = Format().group(True)),
]

columns_total = [
    dict(id="dates", name="일자", type="text", ),
    dict(id="category1", name="구분", type="text"),
    dict(id="category2", name="항목", type="text"),
    dict(id="category3", name="세부항목", type="numeric"),
    dict(id="price", name="금액", type="numeric",  format = Format().group(True)),
    dict(id="unit", name="단위", type="text"),
    dict(id="price_final", name="환산 금액(원)", type="numeric",  format = Format().group(True)),
]

def fetch_all_data():
    conn = sqlite3.connect('raremade.db')
    data = pd.read_sql_query("""
                            SELECT dates, category1, category2, category3, price, unit, 
                             case when unit = '위안' then price * 180 else price end as price_final
                            FROM data order by dates desc
                             """, conn)
    conn.close()
    return data

def fetch_daily_data():
    conn = sqlite3.connect('raremade.db')
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
    
external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
app = Dash(__name__, external_scripts = external_script)
server = app.server
app.scripts.config.serve_locally = True

app.layout = html.Div([
    html.H1(className = 'text-4xl text-center font-bold', children = 'Raremade Management Application'),
    html.Div([
        html.Div([
            html.A("회계장부 입력", className='text-2xl text-left'),
            html.Form([
                html.Label(children="일자"),
                dcc.DatePickerSingle(
                    id="date",
                    date = date.today(),
                    display_format = "YYYY-MM-DD",
                    style = {'display':'block', 'width': "100"}
                ),
                html.Br(),
                html.Div([
                    html.Label('구분'),
                    dcc.Dropdown(['수입','지출'], id="category1",  style = {'width':'50%'}),
                    html.Br(),
                    html.Label('항목'),
                    dcc.Dropdown(id="category2",  style = {'width':'50%'}, className = ""),
                    html.Br(),
                    html.Label('세부항목'),
                    dcc.Input(id="category3",  type="text", placeholder="세부항목", className = "block border rounded-xl px-4 py-2 w-72"),
                    html.Br(),
                    html.Label('금액'),
                    dcc.Input(id = "price", type="number", value=0, placeholder="금액", className = "block border rounded-xl px-4 py-2 w-72", required=True),
                    html.Br(),
                    html.Label('단위'),
                    dcc.Dropdown(['원','위안'], id="price_unit", style={"width": '50%'}, value="원"),
                    html.Br(),
                    html.Label('환산 금액'),
                    html.Span(id="price_transform", style={'display':'block'}),
                ]),
            
                html.Br(),
                html.Button('저장', id="submit", n_clicks=0, className="text-lg font-bold px-4 py-2 border rounded-xl "),
            ], ),
        ], className= "flex flex-col border px-36 py-5 mx-36"),
        
    ], className = "p-5 flex flex-col justify-center"),
    html.Div([
        html.A("전체 기록", className = "text-2xl font-bold mt-10"),
        dash_table.DataTable(
            id="table",
            columns = columns_total,
            data=fetch_all_data().to_dict('records'),
            style_cell_conditional = [
                {'if': {'column_id':c},
                 'textAlign': 'center'}
                 for c in ['dates','category1']
            ],
            style_data_conditional = [
                {
                    'if': {'row_index':'odd'},
                    'backgroundColor': '#E8E8E8',
                }
            ],
            style_header = {'backgroundColor': '#E2E2E2',
                            'color': 'black', 'fontWeight': 'bold', 'textAlign': 'center'})
    ], className = "p-5"),
    html.Div([
        html.A('일별 기록', className = "text-2xl font-bold mt-10"),
        dash_table.DataTable(
            id="daily_table",
            columns = columns_daily,
            data=fetch_daily_data().to_dict('records'),
            style_header = {'backgroundColor': '#E2E2E2',
                            'color': 'black', 'fontWeight': 'bold', 'textAlign': 'center'},
            style_data_conditional = (
                [
                    {
                        'if': {'filter_query': '{{{}}} > 0'.format(col),
                               'column_id' : col},
                        'color': 'blue'
                    } for col in ['daily_revenue'] 
                ] + 
                [
                    {
                        'if': {'filter_query': '{{{}}} <= 0'.format(col),
                               'column_id' : col},
                        'color': 'red'
                    } for col in ['daily_revenue'] 
                ]
            ),
            style_cell_conditional = [
                {'if': {'column_id':c},
                 'textAlign': 'center'}
                 for c in ['dates']
            ]),
    ], className = "p-5")
], className = "p-5")

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
    Output('table','data'),
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
        
    return fetch_all_data().to_dict('records'), fetch_daily_data().to_dict('records')
    
if __name__ == '__main__':
    app.run(debug = True)
