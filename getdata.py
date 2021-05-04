# TICKER별 가격, 거래량 가져오는 함수입니다.
# 수익률, 누적 수익률 산출합니다.

import datetime
import pandas_datareader.data as web
import pandas as pd

TICKER = ['AAPL','TSLA','MSFT','GOOGL','FB']
df = []
for i in range(0,len(TICKER)-1):
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime.now()
    dfs = web.DataReader(TICKER[i], 'yahoo', start, end)
    dfs.reset_index(inplace=True)
    dfs.set_index("Date", inplace=True)
    dfs['Return'] = (dfs['Close'] / dfs['Close'].shift(1)) - 1
    dfs['Return(cum)'] = (1 + dfs['Return']).cumprod()
    dfs.loc[:,'TICKER'] = TICKER[i]
    df.append(pd.DataFrame(dfs))

print(df)
