import os 
import numpy as np
import pandas as pd


def select(df:pd.DataFrame, start_date:str, end_date:str, *args, **kwargs):
    """
    function: select the historical data based on time stamp, make sure the timestamp as the index of dataframe 
    args: {
        1. df: initial dataframe
        2. start_date: YYYY-MM-DD
        3. end_date: YYYY-MM-DD
    }
    """
    next_df = df[df['Date'].between(start_date, end_date, inclusive="both")]
    return next_df.iloc[:, 1:].to_numpy()


def rolling(arr:np.ndarray, window_len:int):
    # fucntion: rolling data
    n_sample = len(arr) - window_len + 1
    return np.array([arr[index:index + window_len] for index in range(len(arr) - window_len)]), n_sample


def convert(root_path:str, start_date:str, end_date:str, window_len:int, *args, **kwargs):
    """
    fucntion: Merge all stock data into four dimensions: asset dimension, date dimension, time window dimension, feature dimension
    """
    latest_arr = []

    for item in os.listdir(root_path):
        next_df = select(df = pd.read_csv(root_path + item),
                        start_date=start_date, 
                        end_date=end_date)
        
        df_matrix, n_sample = rolling(arr=next_df, 
                                      window_len=window_len)
        latest_arr.append(df_matrix)

    lastest_df = np.stack(latest_arr, axis=0)

    np.save('stock_'+kwargs.get("country", "default")+ '_' + str(len(latest_arr)) +'.npy', lastest_df)
    print('data info:', lastest_df.shape)

    # output shape: [n_assets, n_samples, window_len, n_features]
    return lastest_df


if __name__ == '__main__':

   latest_df = convert(
       root_path='data/stock_list/cn/next/', 
       start_date='2020-01-01', 
       end_date='2020-12-31',
       window_len=10, 
       country = 'cn'


   )




  



  
