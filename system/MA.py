import pandas as pd

from indicator.daily.ATR import calculate_atr
from indicator.daily.MA import calculate_ma

import pandas as pd

import pandas as pd


def calculate_trades(df, initial_capital=10000):
    # 初始化变量
    cash = initial_capital
    position = 0  # 当前持有的数量
    trades = []  # 用于存储交易记录

    # 遍历 dataframe
    for i in range(len(df)):
        # 获取当前行的数据
        row = df.iloc[i]

        # 买入条件：ma40 > ma100 且当前没有持仓
        if row['ma40'] > row['ma100'] and position == 0:
            # 计算可买入的数量（100的整数倍）
            buy_price = row['close_value']
            buy_quantity = (cash // buy_price) // 100 * 100
            if buy_quantity > 0:
                # 更新现金和头寸
                cash -= buy_price * buy_quantity
                position = buy_quantity
                # 记录买入信息
                trades.append({
                    '买入时间': row['net_value_date'],
                    '买入价格': buy_price,
                    '买入数量': buy_quantity,
                    '买入头寸': buy_price * buy_quantity,
                    '卖出时间': None,
                    '卖出价格': None,
                    '卖出数量': None,
                    '卖出头寸': None
                })

        # 卖出条件：ma40 < ma100 且当前有持仓
        elif row['ma40'] < row['ma100'] and position > 0:
            # 卖出所有持仓
            sell_price = row['close_value']
            sell_quantity = position
            # 更新现金和头寸
            cash += sell_price * sell_quantity
            position = 0
            # 记录卖出信息
            trades[-1]['卖出时间'] = row['net_value_date']
            trades[-1]['卖出价格'] = sell_price
            trades[-1]['卖出数量'] = sell_quantity
            trades[-1]['卖出头寸'] = sell_price * sell_quantity

    # 将交易记录转换为 dataframe
    trades_df = pd.DataFrame(trades)

    # 合并原始 dataframe 和交易记录
    result_df = pd.concat([df, trades_df], axis=1)

    return result_df




# 示例用法

fund_code = '510300'
# 获取40日均线
result_40 = calculate_ma(fund_code, ma_days=40)
# 获取100日均线
result_100 = calculate_ma(fund_code, ma_days=100)
# 获取ATR
atr_result = calculate_atr(fund_code,period=14)

# 合并40日和100日均线的结果
combined_result = pd.merge(result_40, result_100, on=["fund_code", "net_value_date", "close_value"], how="outer")

# 保存合并后的结果
# combined_result.to_excel('data/MA.xlsx', index=False)

result_df = calculate_trades(combined_result)
print(result_df)
result_df.to_excel('data/MA.xlsx', index=False)
