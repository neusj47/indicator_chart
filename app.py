# -*- coding: utf-8 -*-

# 특정 종목에 대한 가격, 거래량, 수익률을 확인할 수 있는 함수
# 대상 기간과 관심 TICKER를 입력합니다.
# 가격, 거래량 등 Indicator를 설정하여 가격, 거래량 data를 호출합니다. (1차)
# 가격, 거래량 data를 이용하여 Graph를 산출합니다. (2차)

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader.data as web
import datetime


# 기간을 입력합니다.
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime.now()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# 관심 TICKER 데이터를 생성합니다.
TICKER = 'AAPL'
df = web.DataReader(TICKER, 'yahoo', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
df['Return'] = (df['Close'] / df['Close'].shift(1)) - 1
df['Return(cum)'] = (1 + df['Return']).cumprod()
df.loc[:,'TICKER'] = TICKER

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2(children='PRICE-by-VOLUME CHART'),
    html.Div(children='''
    AAPL
    '''),
    dcc.Graph(
        id='clientside-graph'
    ),
    # 구조체의 indicator(ex, Close, Volume) 를 정의합니다.
    'Indicator',
    dcc.Dropdown(
        id='clientside-graph-indicator',
        options=[
            {'label': 'Price', 'value': 'Close'},
            {'label': 'Volume', 'value': 'Volume'},
            {'label': 'Return', 'value': 'Return'}
        ],
        value='Price'
    ),
    # 구조체의 Scale(ex, Linear, Log) 를 정의합니다.
    'Graph scale',
    dcc.RadioItems(
        id='clientside-graph-scale',
        options=[
            {'label': x, 'value': x} for x in ['linear', 'log']
        ],
        value='linear'
    ),
    # 구조체의 산출물(data)을 정의합니다.
    dcc.Store(
        id='clientside-figure-store',
        data=[{
            'x': df.index,
            'y': df['Close']
        }]
    ),
    html.Hr()
])

# 반응형으로 작동하는 1차 callback 함수를 정의합니다.
# Input : indicator ex) 가격, 거래량
# Output : data     ex) 가격 data, 거래량 data
@app.callback(
    Output('clientside-figure-store', 'data'),
    Input('clientside-graph-indicator', 'value')
)
def update_store_data(indicator):
    return [{
        'x': df.index,
        'y': df[indicator],
        # 'mode': 'markers'
    }]

# 반응형으로 작동하는 2차 callback 함수를 정의합니다.
# Input : indicator ex) 가격, 거래량, 가격 data, 거래량 data
# Output : graph
app.clientside_callback(
    """
    function(data, scale) {
        return {
            'data': data,
            'layout': {
                 'yaxis': {'type': scale}
             }
        }
    }
    """,
    Output('clientside-graph', 'figure'),
    Input('clientside-figure-store', 'data'),
    Input('clientside-graph-scale', 'value')
)

if __name__ == '__main__':
    app.run_server(debug=True)