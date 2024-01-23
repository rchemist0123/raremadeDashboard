from dash import html, dcc, dash_table
from dash.dash_table.Format import Format, Group
from datetime import date
from functions import fetch_daily_data

def create_layout() :
    columns_daily = [
        dict(id="dates", name="일자"),
        dict(id="income", name="수입", type = "numeric", format = Format().group(True)),
        dict(id="expenditure", name="지출",  type = "numeric", format = Format().group(True)),
        dict(id="daily_revenue", name="일일정산",  type = "numeric", format = Format().group(True)),
    ]

    # columns_total = [
    #     dict(id="dates", name="일자", type="text", ),
    #     dict(id="category1", name="구분", type="text"),
    #     dict(id="category2", name="항목", type="text"),
    #     dict(id="category3", name="세부항목", type="numeric"),
    #     dict(id="price", name="금액", type="numeric",  format = Format().group(True)),
    #     dict(id="unit", name="단위", type="text"),
    #     dict(id="price_final", name="환산 금액(원)", type="numeric",  format = Format().group(True)),
    # ]

    return html.Div([
        html.H1(className = 'text-4xl text-center font-bold my-10', children = 'Raremade Management Application'),
        html.Div([
            html.Div([
                html.P("회계장부 입력", className='text-2xl text-left w-36'),
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
                        dcc.Dropdown(['수입','지출'], id="category1", className = "w-72"),
                        html.Br(),
                        html.Label('항목'),
                        dcc.Dropdown(id="category2", className = "w-72"),
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
                    html.Div([
                        html.Button('저장', 
                                    id="submit", 
                                    n_clicks=0, 
                                    className="text-lg font-bold px-4 py-2 border rounded-xl md:w-36"),
                    ], className = "flex flex-col justify-center")
                ]),
            ], className= "flex flex-col justify-center"),
        ], className = "p-5 flex"),
        html.Div([
            html.P('일별 기록', className = "text-2xl font-bold my-5"),
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
        ], className = "p-5"),
        html.Div([
            html.P('전체 기록 다운로드', className = "text-2xl font-bold my-5"),
            html.Button("Download CSV", id="btn_csv", className = "border rounded-xl py-2 px-3 md:w-36"),
            dcc.Download(id="download_csv"),
        ], className = "p-5 flex flex-col justify-center")
    ], className = "p-5")

