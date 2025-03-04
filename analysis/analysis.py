import pandas as pd
import numpy as np

def analyze_trades(df):
    trades = []

    # 遍历 DataFrame 按行进行处理
    for i in range(len(df)):
        # 查找买入信号
        if pd.notna(df.loc[i, 'buy_time']):
            buy_time = df.loc[i, 'buy_time']
            buy_price = df.loc[i, 'buy_price']
            buy_quantity = df.loc[i, 'buy_quantity']
            buy_total = df.loc[i, 'buy_total']
            buy_capital = df.loc[i, 'capital']  # 记录买入时的资产总额

            # 寻找下一行的卖出信号
            sell_row = df.iloc[i + 1:] if i + 1 < len(df) else pd.DataFrame()
            sell_row = sell_row[sell_row['sell_time'].notna()]

            if not sell_row.empty:
                sell_time = sell_row.iloc[0]['sell_time']
                sell_price = sell_row.iloc[0]['sell_price']
                sell_quantity = sell_row.iloc[0]['sell_quantity']
                sell_total = sell_row.iloc[0]['sell_total']
                sell_capital = sell_row.iloc[0]['capital']  # 记录卖出时的资产总额

                # 计算持有时间
                holding_time = (sell_time - buy_time).days

                # 计算盈利金额
                profit = (sell_price - buy_price) * buy_quantity

                # 计算盈利比率
                profit_ratio = profit / (buy_price * buy_quantity)

                # 记录买入时和卖出后的资产总额
                trades.append({
                    'buy_time': buy_time,
                    'sell_time': sell_time,
                    'holding_time': holding_time,
                    'profit': profit,
                    'profit_ratio': profit_ratio,
                    'capital': sell_capital  # 卖出时的资产总额
                })

    # 返回交易结果的 DataFrame
    return pd.DataFrame(trades)


import pandas as pd
import numpy as np


def analyze_trades_and_calculate_metrics(df):
    if df.empty:
        return None

    # 初始资金取自第一行 capital
    initial_capital = df.iloc[0]['capital']

    trades = []
    max_consecutive_losses = 0
    current_losses = 0

    for i in range(len(df)):
        if pd.notna(df.loc[i, 'buy_time']):
            buy_time = df.loc[i, 'buy_time']
            buy_price = df.loc[i, 'buy_price']
            buy_quantity = df.loc[i, 'buy_quantity']
            buy_total = df.loc[i, 'buy_total']
            buy_capital = df.loc[i, 'capital']

            sell_row = df.iloc[i + 1:] if i + 1 < len(df) else pd.DataFrame()
            sell_row = sell_row[sell_row['sell_time'].notna()]

            if not sell_row.empty:
                sell_time = sell_row.iloc[0]['sell_time']
                sell_price = sell_row.iloc[0]['sell_price']
                sell_quantity = sell_row.iloc[0]['sell_quantity']
                sell_total = sell_row.iloc[0]['sell_total']
                sell_capital = sell_row.iloc[0]['capital']

                holding_time = (sell_time - buy_time).days
                profit = (sell_price - buy_price) * buy_quantity
                profit_ratio = profit / (buy_price * buy_quantity)

                trades.append({
                    'Type': 'Trade',
                    'buy_time': buy_time,
                    'sell_time': sell_time,
                    'holding_time': holding_time,
                    'profit': profit,
                    'profit_ratio': profit_ratio,
                    'capital': sell_capital
                })

                # 计算最大连输次数
                if profit < 0:
                    current_losses += 1
                    max_consecutive_losses = max(max_consecutive_losses, current_losses)
                else:
                    current_losses = 0

    trades_df = pd.DataFrame(trades)

    if trades_df.empty:
        return None

    # 计算总收益率
    final_capital = trades_df.iloc[-1]['capital']
    total_return = (final_capital - initial_capital) / initial_capital

    # 计算交易时间跨度（天数）
    total_days = (trades_df['sell_time'].max() - trades_df['buy_time'].min()).days
    annualized_return = (1 + total_return) ** (252 / total_days) - 1 if total_days > 0 else 0

    # 计算最大回撤
    capital_series = trades_df['capital']
    max_drawdown = np.max(
        (np.maximum.accumulate(capital_series) - capital_series) / np.maximum.accumulate(capital_series))

    # 计算胜率
    win_rate = (trades_df['profit'] > 0).mean()

    # 计算平均盈利比率 & 平均亏损比率
    avg_profit_ratio = trades_df.loc[trades_df['profit'] > 0, 'profit_ratio'].mean()
    avg_loss_ratio = trades_df.loc[trades_df['profit'] < 0, 'profit_ratio'].mean()

    # 指标数据转换为 DataFrame，并增加 Type 字段
    metrics_df = pd.DataFrame([{
        "Type": "Metrics",
        "Annualized Return": annualized_return,
        "Max Drawdown": max_drawdown,
        "Win Rate": win_rate,
        "Average Profit Ratio": avg_profit_ratio,
        "Average Loss Ratio": avg_loss_ratio,
        "Max Consecutive Losses": max_consecutive_losses
    }])

    # 合并两个 DataFrame
    combined_df = pd.concat([trades_df, metrics_df], ignore_index=True)

    return combined_df




# df = pd.read_excel('../system/data/MA.xlsx')
#
# # 执行分析
# result_df = analyze_trades(df)
#
# # 输出分析结果
# print(result_df)
