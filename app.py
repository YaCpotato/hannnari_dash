import numpy as np
import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
from sklearn.datasets import load_boston
import pandas as pd

import plotly.graph_objs as go
import plotly.figure_factory as ff

boston = load_boston()
boston_df = pd.DataFrame(boston.data, columns=boston.feature_names)
boston_df['MEDV'] = boston.target
corr = boston_df.corr()

boston_df_exp = [
    '犯罪発生率',
    '25,000平方フィート以上の住宅区画の割合',
    '非小売業種の土地面積の割合',
    'チャールズ川沿いか否か',
	  '窒素酸化物の濃度',
    '平均部屋数',
    '1940年より前に建てられた建物の割合',
    '5つのボストンの雇用施設への重み付き距離',
    '高速道路へのアクセスのしやすさ',
    '10,000ドルあたりの不動産税率',
    '生徒と教師の割合',
    '黒人の割合',
    '低所得者の割合',
]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


content = html.Div(id="page-content")

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='データソース', value='tab-1'),
        dcc.Tab(label='グラフビュー', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dash_table.DataTable(
                                id = 'data_table',
                                columns = [{"name": i, "id": j} for i,j in zip(boston_df,boston_df.columns)],
                                data = boston_df.to_dict('records'),
                                page_size = 10
                            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph( 
                figure = ff.create_annotated_heatmap(
                    z = np.round(corr.values, decimals=2),
                    x = boston_df.columns.values.tolist(),
                    y = boston_df.columns.values.tolist(),
                    colorscale='Magma',showscale=True).update_yaxes(autorange="reversed"
                )
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
