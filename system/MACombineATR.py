import pandas as pd

from analysis.analysis import analyze_trades_and_calculate_metrics
from indicator.daily.ATR import calculate_atr
from indicator.daily.MA import calculate_ma


def execute_trades_with_atr(df, initial_capital=10000, trade_size=100, atr_multiplier=2):
    df = df.sort_values(by='net_value_date').reset_index(drop=True)

    df['stop_loss'] = None
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
    stop_loss = None

    for idx in range(len(df) - 1):  # 遍历到倒数第二行，确保可以取到下一天数据
        row = df.iloc[idx]
        next_day = df.iloc[idx + 1]

        if position > 0 and row['low_value'] <= stop_loss:  # 触发止损卖出
            sell_price = stop_loss  # 止损价卖出
            sell_date = row['net_value_date']
            sell_quantity = position

            df.at[idx, 'sell_time'] = sell_date
            df.at[idx, 'sell_price'] = sell_price
            df.at[idx, 'sell_quantity'] = sell_quantity
            df.at[idx, 'sell_total'] = sell_quantity * sell_price

            capital += sell_quantity * sell_price
            position = 0
            stop_loss = None  # 清除止损价

        if row['ma5'] > row['ma10'] and position == 0:  # 触发买入信号
            buy_quantity = (capital // next_day['open_value']) // trade_size * trade_size
            if buy_quantity > 0:
                buy_price = next_day['open_value']
                buy_date = next_day['net_value_date']
                stop_loss = buy_price - atr_multiplier * row['ATR14']

                df.at[idx, 'buy_time'] = buy_date
                df.at[idx, 'buy_price'] = buy_price
                df.at[idx, 'buy_quantity'] = buy_quantity
                df.at[idx, 'buy_total'] = buy_quantity * buy_price
                df.at[idx, 'stop_loss'] = stop_loss

                capital -= buy_quantity * buy_price
                position = buy_quantity

        elif row['ma5'] < row['ma10'] and position > 0:  # 触发卖出信号
            sell_price = next_day['open_value']
            sell_date = next_day['net_value_date']
            sell_quantity = position

            df.at[idx, 'sell_time'] = sell_date
            df.at[idx, 'sell_price'] = sell_price
            df.at[idx, 'sell_quantity'] = sell_quantity
            df.at[idx, 'sell_total'] = sell_quantity * sell_price

            capital += sell_quantity * sell_price
            position = 0
            stop_loss = None  # 清除止损价

        # 更新资金总量（包括持仓市值）
        df.at[idx, 'capital'] = capital + position * row['close_value']

    return df

# 示例调用
# df = execute_trades_with_atr(your_dataframe)
# print(df)

fund_code = '510300'
ma_short_days = 28
ma_long_days = 110
atr_multiplier = 2
# 获取均线数据
result_short = calculate_ma(fund_code, ma_days=ma_short_days)
result_long = calculate_ma(fund_code, ma_days=ma_long_days)
# 获取ATR
atr_result = calculate_atr(fund_code,period=14)
# 合并40日和100日均线的结果
combined_result = pd.merge(result_short, result_long, on=["fund_code", "net_value_date", "close_value", "open_value"], how="outer")
combined_result = pd.merge(combined_result, atr_result, on=["fund_code", "net_value_date", "close_value", "open_value"], how="outer")

result_df = execute_trades_with_atr(combined_result,atr_multiplier)
analysis = analyze_trades_and_calculate_metrics(result_df)

# 保存
# 定义 Excel 文件路径，包含日期信息
file_path = f'data/MACombineATR_{ma_short_days}_{ma_long_days}_{atr_multiplier}.xlsx'
# 使用 ExcelWriter 保存多个 Sheet
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    result_df.to_excel(writer, sheet_name='Trades', index=False)  # 交易数据
    analysis.to_excel(writer, sheet_name='Analysis', index=False)  # 分析结果

print(f'数据已成功保存至 {file_path}')
# 打印结果
print(result_df)
