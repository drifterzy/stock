import pandas as pd

from indicator.daily.ATR import calculate_atr
from indicator.daily.MA import calculate_ma


def execute_trades(df, initial_capital=10000, trade_size=100):
    df['buy_time'] = None
    df['buy_price'] = None
    df['buy_quantity'] = None
    df['buy_total'] = None
    df['sell_time'] = None
    df['sell_price'] = None
    df['sell_quantity'] = None
    df['sell_total'] = None
    df['capital'] = initial_capital

    capital = initial_capital
    position = 0
    buy_price = 0
    buy_date = None

    for idx, row in df.iterrows():
        if row['ma20'] > row['ma60'] and position == 0:
            # Buy signal
            buy_quantity = (capital // row['close_value']) // trade_size * trade_size
            if buy_quantity > 0 and idx + 1 < len(df):  # Ensure there's a next row (second day's open price)
                # Buy price is the next day's open price
                next_day_open = df.iloc[idx + 1]['open_value']
                next_day_date = df.iloc[idx + 1]['net_value_date']
                df.at[idx, 'buy_time'] = next_day_date  # Buy time is the next day's date
                df.at[idx, 'buy_price'] = next_day_open
                df.at[idx, 'buy_quantity'] = buy_quantity
                df.at[idx, 'buy_total'] = buy_quantity * next_day_open
                position = buy_quantity
                capital -= buy_quantity * next_day_open
                buy_price = next_day_open
                buy_date = next_day_date

        elif row['ma20'] < row['ma60'] and position > 0:
            # Sell signal
            if idx + 1 < len(df):  # Ensure there's a next row (second day's open price)
                # Sell price is the next day's open price
                next_day_open = df.iloc[idx + 1]['open_value']
                next_day_date = df.iloc[idx + 1]['net_value_date']
                sell_quantity = position
                df.at[idx, 'sell_time'] = next_day_date  # Sell time is the next day's date
                df.at[idx, 'sell_price'] = next_day_open
                df.at[idx, 'sell_quantity'] = sell_quantity
                df.at[idx, 'sell_total'] = sell_quantity * next_day_open
                capital += sell_quantity * next_day_open
                position = 0

        # Update capital remaining
        df.at[idx, 'capital'] = capital + position * row['close_value']

    return df


# 示例用法

fund_code = '510300'
# 获取20日均线
result_20 = calculate_ma(fund_code, ma_days=20)
# 获取60日均线
result_60 = calculate_ma(fund_code, ma_days=60)
# 获取ATR
atr_result = calculate_atr(fund_code, period=14)

# 合并20日和60日均线的结果
combined_result = pd.merge(result_20, result_60, on=["fund_code", "net_value_date", "close_value", "open_value"], how="outer")

# 执行交易
result_df = execute_trades(combined_result)

# 打印结果
print(result_df)

# 保存结果到Excel文件
result_df.to_excel('data/MA20.xlsx', index=False)
