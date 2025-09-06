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

### 东方财富网

#### 一级股吧评论数据
```python
{
    "贴吧名称": "上证指数吧",
    "贴文id": 1595850067,
    "贴文类型": 0,
    "发布时间": "2025-09-05 15:07:28",
    "发表时间戳": "",
    "贴文标题": "开始日期：2023年5月1日，初始资金：120万，朋友盈亏：十8700，本人盈亏",
    "作者id": "5613093981596062",
    "作者名称": "疯皇捏盘",
    "阅读数": 6751,
    "评论数": 276,
    "评论": [……]
}
```

##### 二级股吧评论数据
```python
评论": [
      {
        "评论id": 9763659222,
        "评论时间": "2025-09-06 21:33:00",
        "评论者id": "8820014645298842",
        "评论者昵称": "好想抓牛股",
        "年限": "9.4年",
        "地点": "浙江",
        "评论内容": "韭菜又不是什么侮辱性的词，股市里韭菜这个词很正常。又是gun又是狗的，幸好我截图了，不然口说无凭。这种侮辱性的骂人疯皇你怎么处理？不管就是鼓励大家以后骂人咯？ ",
        "回复": null
      },
      {
        "评论id": 9763657265,
        "评论时间": "2025-09-06 21:24:58",
        "评论者id": "5548336238134818",
        "评论者昵称": "阳均三年消险",
        "年限": "4.3年",
        "地点": "广东",
        "评论内容": "一秒钟下单3000次是硅谷量化的平均运算效率。 ",
        "回复": null
      },
      {
        "评论id": 9763655546,
        "评论时间": "2025-09-06 21:18:04",
        "评论者id": "9440013465636044",
        "评论者昵称": "和气成金趋势为王",
        "年限": "13.2年",
        "地点": "安徽",
        "评论内容": "如果说：说真的，以前看你有个P图的徒弟就知道师傅啥样了。这句话就是你口中的满口恶语，我只能说你太那啥了 ",
        "回复": null
      },
      {
        "评论id": 9763653134,
        "评论时间": "2025-09-06 21:08:34",
        "评论者id": "9440013465636044",
        "评论者昵称": "和气成金趋势为王",
        "年限": "13.2年",
        "地点": "安徽",
        "评论内容": "我在东财只拉黑过2个人，一个是喜欢p图的，一个就是看不起别人的，道不同不相为谋 ",
        "回复": [
          {
            "回复id": 9763660768,
            "回复者id": "9440013465636044",
            "回复者地址": "安徽",
            "回复时间": "2025-09-06 21:39:23",
            "回复内容": "今晚最后一次发帖，明天开始沉下心来操作，不达到目标不回来 "
          },
          {
            "回复id": 9763660558,
            "回复者id": "5548336238134818",
            "回复者地址": "广东",
            "回复时间": "2025-09-06 21:38:33",
            "回复内容": "从平台拿推广费的人，一般至少十多个不同的马甲，不同马甲之间互相掩护和造势。 "
          }
        ]
      },
```
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Liangwei-0521/Easy_Finance_Data&type=Date)](https://star-history.com/#Liangwei-0521/Easy_Finance_Data&Date)
