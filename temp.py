html.Div([
        html.A("전체 기록 다운로드", className = "text-2xl font-bold mt-10"),
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
            style_table={'overflowX': 'auto'},
            style_cell = {
                'height': 'auto',
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            style_header = {'backgroundColor': '#E2E2E2',
                            'color': 'black', 'fontWeight': 'bold', 'textAlign': 'center'})
    ], className = "p-5"),