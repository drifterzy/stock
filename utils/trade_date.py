import akshare as ak
import pandas as pd
from utils.file_tool import save_dataframe_to_excel

tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()

# 转换日期列的数据类型为 datetime
tool_trade_date_hist_sina_df['trade_date'] = pd.to_datetime(tool_trade_date_hist_sina_df['trade_date'])

# 创建一个空的DataFrame用于存储结果
nearest_trade_dates = pd.DataFrame(columns=['reference_date', 'nearest_trade_date'])

# 循环处理每个月15号的数据
for month in range(1, 9):
    target_date = pd.Timestamp(year=2023, month=month, day=15)
    relevant_dates = tool_trade_date_hist_sina_df[
        (tool_trade_date_hist_sina_df['trade_date'] >= target_date) &
        (tool_trade_date_hist_sina_df['trade_date'].dt.year == 2023)
    ]
    if not relevant_dates.empty:
        nearest_date = relevant_dates.iloc[0]['trade_date']
        nearest_trade_dates = nearest_trade_dates.append({'reference_date': target_date, 'nearest_trade_date': nearest_date}, ignore_index=True)

# 打印结果
print(nearest_trade_dates['nearest_trade_date'])
