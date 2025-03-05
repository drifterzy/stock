import pandas as pd

from analysis.analysis import analyze_trades_and_calculate_metrics
from indicator.daily.ATR import calculate_atr
from indicator.daily.MA import calculate_ma

import pandas as pd



def trading_strategy(df, ma_short_days=5, ma_long_days=10, ma_max_days=40):
    initial_cash = 10000  # 初始资金
    cash = initial_cash  # 当前资金
    position = 0  # 当前持仓数量

    short_col = f'ma{ma_short_days}'
    long_col = f'ma{ma_long_days}'
    max_col = f'ma{ma_max_days}'

    df = df.sort_values(by="net_value_date")  # 按日期排序，确保时间顺序正确
    df["buy_time"] = None
    df["buy_price"] = None
    df["buy_quantity"] = None
    df["buy_total"] = None
    df["sell_time"] = None
    df["sell_price"] = None
    df["sell_quantity"] = None
    df["sell_total"] = None
    df["capital"] = None

    for i in range(len(df) - 1):  # 遍历到倒数第二天（因为买入、卖出价格是第二天的开盘价）
        today = df.iloc[i]
        next_day = df.iloc[i + 1]

        # 买入逻辑
        if position == 0 and today[short_col] > today[long_col] and today[short_col] > today[max_col] and today[
            long_col] > today[max_col]:
            buy_price = next_day["open_value"]
            max_shares = (cash // (buy_price * 100)) * 100  # 计算可买的最大股数（100的整数倍）
            if max_shares > 0:
                cost = max_shares * buy_price
                cash -= cost
                position += max_shares

                df.at[i + 1, "buy_time"] = next_day["net_value_date"]
                df.at[i + 1, "buy_price"] = buy_price
                df.at[i + 1, "buy_quantity"] = max_shares
                df.at[i + 1, "buy_total"] = cost

        # 卖出逻辑
        elif position > 0 and today[short_col] < today[long_col]:
            sell_price = next_day["open_value"]
            revenue = position * sell_price
            cash += revenue

            df.at[i + 1, "sell_time"] = next_day["net_value_date"]
            df.at[i + 1, "sell_price"] = sell_price
            df.at[i + 1, "sell_quantity"] = position
            df.at[i + 1, "sell_total"] = revenue

            position = 0  # 清空持仓

        # 记录资金总量
        df.at[i, "capital"] = cash + (position * today["close_value"] if position > 0 else 0)

    # 处理最后一天的资金总量
    last_close = df.iloc[-1]["close_value"]
    df.at[len(df) - 1, "capital"] = cash + (position * last_close if position > 0 else 0)

    return df


fund_code = '510300'
ma_short_days = 5
ma_long_days = 10
# atr_multiplier = 5
best_ma_max = None
max_capital = float('-inf')
for ma_max_days in range(40, 101):
    result_short = calculate_ma(fund_code, ma_days=ma_short_days)
    result_long = calculate_ma(fund_code, ma_days=ma_long_days)
    result_max = calculate_ma(fund_code, ma_days=ma_max_days)

    combined_result = pd.merge(result_short, result_long,
                               on=["fund_code", "net_value_date", "close_value", "open_value"], how="outer")
    combined_result = pd.merge(combined_result, result_max,
                               on=["fund_code", "net_value_date", "close_value", "open_value"], how="outer")

    result_df = trading_strategy(combined_result, ma_short_days=ma_short_days, ma_long_days=ma_long_days,
                                 ma_max_days=ma_max_days)
    final_capital = result_df['capital'].iloc[-1]

    if final_capital > max_capital:
        max_capital = final_capital
        best_ma_max = ma_max_days


result_short = calculate_ma(fund_code, ma_days=ma_short_days)
result_long = calculate_ma(fund_code, ma_days=ma_long_days)
result_max = calculate_ma(fund_code, ma_days=best_ma_max)
# 获取ATR
# atr_result = calculate_atr(fund_code, period=14)
# 合并均线和ATR的结果
combined_result = pd.merge(result_short, result_long, on=["fund_code", "net_value_date", "close_value", "open_value"], how="outer")
combined_result = pd.merge(combined_result, result_max, on=["fund_code", "net_value_date", "close_value", "open_value"], how="outer")
# combined_result = pd.merge(combined_result, atr_result, on=["fund_code", "net_value_date", "close_value", "open_value"], how="outer")

result_df = trading_strategy(combined_result, ma_short_days=ma_short_days, ma_long_days=ma_long_days,ma_max_days = best_ma_max)
analysis = analyze_trades_and_calculate_metrics(result_df)

# 保存到 Excel
file_path = f'data/MATriple_{ma_short_days}_{ma_long_days}_{best_ma_max}.xlsx'
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    result_df.to_excel(writer, sheet_name='Trades', index=False)  # 交易数据
    analysis.to_excel(writer, sheet_name='Analysis', index=False)  # 分析结果

print(f'数据已成功保存至 {file_path}')
print(result_df)
