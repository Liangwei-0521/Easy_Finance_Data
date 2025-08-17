# Easy Finance Data

#### Designate industry index constituent stocks and easily obtain price, technical factor and other indicator data based on Yahoo Finance to facilitate strategy model training and testing.

## Example 

### * HK Market
```python
import pandas as pd 

hsi_list = pd.read_csv('./data/stock_list/hk/hsi_components.csv')
hsi_list = hsi_list.drop(columns=['Unnamed: 0'])
hsi_list

	code	name
0	00005	汇丰控股
1	00939	建设银行
2	01299	友邦保险
3	01398	工商银行
4	00388	香港交易所
...	...	...
80	01177	中国生物制药
81	00241	阿里健康
82	03692	翰森制药
83	01099	国药控股
84	02359	药明康德
85 rows × 2 columns
```
 
 ### * CN Market
 ```python 
 import pandas as pd

cn_stock_name = pd.read_csv('./data/stock_list/cn/csi100_components.csv')

for item in cn_stock_name['Stock Name']:
    print('股票：', item)
    name = item.split('.')[0] + '.ss'
    print(name)


股票： 600012.XSHG
600012.ss
股票： 600060.XSHG
600060.ss
股票： 600132.XSHG
600132.ss
股票： 600161.XSHG
600161.ss
股票： 600211.XSHG
600211.ss
……

```
## Method 

### * get all the component stock 
```python
# start_date: YYYY-MM-DD end_date: YYYYY-MM-DD
import pandas as pd
import yfinance
from yfinance import *

cn_stock_name = pd.read_csv('./data/stock_list/cn/csi100_components.csv')
start_date = '2016-07-01'
end_date = '2025-08-01'

num = 0 
wrong = 0 

for item in cn_stock_name['Stock Name']:
    print('股票：', item)
    name = item.split('.')[0] + '.ss'

    try:
        # get the data of component stock in DJIA 
        stock = Ticker(ticker=name)
        df = stock.history(start=start_date, end=end_date)
        num = num + 1
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
        if len(df) == 2205: 
            df.to_csv('./data/stock_list/cn/stock/'+item.split('.')[0]+'_ss.csv')
            print('num', num)
            print('the length of data:', len(df))

    except Exception as e:
        wrong = wrong + 1
        print('wrong: ', wrong)
        print(f"Error processing stock {item}: {e}")


```
attention : 2205 is the maximum number of trading days known in advance within a given time range.


### * get technical factor data 
```python 
def add_tech_factor(path):
    """
    function: Incorporate technological factors into the initial dataset
    """
    df = pd.read_csv(path)

    # trend factor
    sma = talib.SMA(df['Close'], timeperiod=20)
    ema = talib.EMA(df['Close'], timeperiod=20)
    macd = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]
    adx = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
    sar = talib.SAR(df['High'], df['Low'], acceleration=0.02, maximum=0.2)

    # momentum factor
    rsi = talib.RSI(df['Close'], timeperiod=14)
    roc = talib.ROC(df['Close'], timeperiod=12)
    cci = talib.CCI(df['High'], df['Low'], df['Close'], timeperiod=20)

    # volatility factor
    atr = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
    # 布林带
    bbans = talib.BBANDS(df['Close'], 
                        timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    # 布林线上轨
    bbans_upper = bbans[0]
    # 布林线中轨
    bbans_middle = bbans[1]
    # 布林线下轨
    bbans_lower = bbans[-1]
    obv = talib.OBV(df['Close'], df['Volume'])
    mfi = talib.MFI(df['High'], df['Low'], df['Close'], df['Volume'], timeperiod=14)

    next_df = df[['Date', 'Open', 'High', 'Low'	,'Close', 'Volume']]

    next_df["SMA"] = sma
    next_df["EMA"] = ema
    next_df["MACD"] = macd
    next_df["ADX"] = adx
    next_df["SAR"] = sar

    next_df["RSI"] = rsi
    next_df["ROC"] = roc
    next_df["CCI"] = cci

    next_df["ATR"] = atr
    next_df["Bbands_Upper"] = bbans_upper
    next_df["Bbands_Middle"] = bbans_middle 
    next_df["Bbands_Lower"] = bbans_lower 
    next_df["OBV"] = obv
    next_df["MFI"] = mfi

    next_df = next_df.set_index("Date")
    next_df.index = pd.to_datetime(next_df.index)

    next_df = next_df.loc["2016-09-01":].copy() 
    return next_df
```

## Next verison
Implementing the acquisition of financial text data