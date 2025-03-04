import pandas as pd
import itertools

from analysis.analysis import analyze_trades
from indicator.daily.ATR import calculate_atr
from indicator.daily.MA import calculate_ma


def execute_trades(df, ma_short_days, ma_long_days, initial_capital=10000, trade_size=100):
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

    short_col = f'ma{ma_short_days}'
    long_col = f'ma{ma_long_days}'

    for idx, row in df.iterrows():
        if row[short_col] > row[long_col] and position == 0:
            buy_quantity = (capital // row['close_value']) // trade_size * trade_size
            if buy_quantity > 0 and idx + 1 < len(df):
                next_day_open = df.iloc[idx + 1]['open_value']
                next_day_date = df.iloc[idx + 1]['net_value_date']
                df.at[idx, 'buy_time'] = next_day_date
                df.at[idx, 'buy_price'] = next_day_open
                df.at[idx, 'buy_quantity'] = buy_quantity
                df.at[idx, 'buy_total'] = buy_quantity * next_day_open
                position = buy_quantity
                capital -= buy_quantity * next_day_open
                buy_price = next_day_open
                buy_date = next_day_date

        elif row[short_col] < row[long_col] and position > 0:
            if idx + 1 < len(df):
                next_day_open = df.iloc[idx + 1]['open_value']
                next_day_date = df.iloc[idx + 1]['net_value_date']
                sell_quantity = position
                df.at[idx, 'sell_time'] = next_day_date
                df.at[idx, 'sell_price'] = next_day_open
                df.at[idx, 'sell_quantity'] = sell_quantity
                df.at[idx, 'sell_total'] = sell_quantity * next_day_open
                capital += sell_quantity * next_day_open
                position = 0

        df.at[idx, 'capital'] = float(capital + position * row['close_value'])

    return df


# 示例用法
fund_code = '510300'
short_ma_range = range(5, 50, 1)
long_ma_range = range(50, 200, 1)
best_params = None
best_capital = 0

for ma_short_days, ma_long_days in itertools.product(short_ma_range, long_ma_range):
    if ma_short_days >= ma_long_days:
        continue

    result_short = calculate_ma(fund_code, ma_days=ma_short_days)
    result_long = calculate_ma(fund_code, ma_days=ma_long_days)

    combined_result = pd.merge(result_short, result_long,
                               on=["fund_code", "net_value_date", "close_value", "open_value"], how="outer")

    result_df = execute_trades(combined_result, ma_short_days, ma_long_days)
    final_capital = result_df['capital'].iloc[-1]

    if final_capital > best_capital:
        best_capital = final_capital
        best_params = (ma_short_days, ma_long_days)

best_ma_short_days, best_ma_long_days = best_params

result_short = calculate_ma(fund_code, ma_days=best_ma_short_days)
result_long = calculate_ma(fund_code, ma_days=best_ma_long_days)

combined_result = pd.merge(result_short, result_long, on=["fund_code", "net_value_date", "close_value", "open_value"],
                           how="outer")

result_df = execute_trades(combined_result, best_ma_short_days, best_ma_long_days)
analysis = analyze_trades(result_df)

file_path = f'data/MA_Trades_{best_ma_short_days}_{best_ma_long_days}.xlsx'

with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    result_df.to_excel(writer, sheet_name='Trades', index=False)
    analysis.to_excel(writer, sheet_name='Analysis', index=False)

print(f'最佳均线组合: {best_ma_short_days}, {best_ma_long_days}，最终资金: {best_capital}')
print(f'数据已成功保存至 {file_path}')
print(result_df)
