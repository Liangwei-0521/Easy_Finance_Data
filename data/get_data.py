import talib
import pandas as pd
from yfinance import *



def get_cn_stock(cn_stock_list: list, 
                 start_date:str, end_date:str, 
                 root_path:str, max_len:int):
    """
    args: cn_stock_list: the components of csi 100
          start_date: the format is YYY-MM-DD
          end_date: the format is YYY-MM-DD
          root_path: data\stock_list\cn\stock,
          max_len: the Maximum number of transaction dates
          
    """
    for item in cn_stock_list['Stock Name']:
        print('stock: ', item)
        name = item.split('.')[0] + '.ss'

        try:
            # get the data of component stock in DJIA 
            stock = Ticker(ticker=name)
            df = stock.history(start=start_date, end=end_date)
            num = num + 1
            df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
            if len(df) == max_len: 
                df.to_csv(root_path+item.split('.')[0]+'_ss.csv')
                print('num', num)
                print('the length of data:', len(df))

        except Exception as e:
            wrong = wrong + 1
            print('wrong: ', wrong)
            print(f"Error processing stock {item}: {e}")



def get_hsi_stock():

    pass 


def get_us_stock(us_stock_list: list, 
                 start_date:str, end_date:str,
                 root_path:str):
    """
    args: ……
    """
    for item in us_stock_list:
        print('stock:', item)

        try:
            # get the data of component stock in DJIA 
            stock = Ticker(ticker=item)
            df = stock.history(start=start_date, end=end_date)
            num = num + 1
            df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
            df.to_csv(root_path+item+'.csv')
            print('sucessful: ', num, 'name', )
            print('the length of data:', len(df))

        except Exception as e:
            wrong = wrong + 1
            print('wrong: ', wrong, 'name: ', item)
            print(f"Error processing stock {item}: {e}")

        return df



def add_tech_factor(path):
    """
    function: Incorporate technological factors into the initial dataset
    """
    # initial data
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




if __name__ == '__main__':
    
    import os 
    import warnings
    warnings.filterwarnings('ignore')

    for item in os.listdir('./data/stock_list/us/stock/'):
        print(item)
        next_df = add_tech_factor(
            path = './data/stock_list/us/stock/'+ item
        )
        next_df.to_csv('./data/stock_list/us/next/'+ item, float_format="%.3f")







