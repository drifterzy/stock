import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt


# 加载数据
def load_data(symbol,start="20200101",end="20250122"):
    """
    使用 akshare 加载股票历史数据并适配格式。

    参数:
    - symbol: 股票代码

    返回:
    - 处理后的 DataFrame
    """
    stock_zh_a_hist_df = ak.stock_zh_a_hist(
        symbol=symbol, period="daily", start_date=start, end_date=end, adjust="hfq"
    )
    stock_zh_a_hist_df.rename(
        columns={
            "日期": "date",
            "开盘": "open",
            "收盘": "close",
            "最高": "high",
            "最低": "low",
        },
        inplace=True,
    )
    stock_zh_a_hist_df['date'] = pd.to_datetime(stock_zh_a_hist_df['date'])
    stock_zh_a_hist_df.set_index('date', inplace=True)
    return stock_zh_a_hist_df[['open', 'close', 'high', 'low']]  # 仅保留必要的列


# 生成交易信号
def turtle_signals(data, n_entry=20, n_exit=10):
    """
    生成交易信号。

    参数:
    - data: 原始数据
    - n_entry: 入场信号的天数窗口
    - n_exit: 出场信号的天数窗口

    返回:
    - 包含信号的 DataFrame
    """
    data['entry_high'] = data['high'].rolling(window=n_entry).max()
    data['exit_low'] = data['low'].rolling(window=n_exit).min()

    # 买入信号：当天最高价 > 昨天的 n_entry 天最高值
    data['long_signal'] = data['high'] > data['entry_high'].shift(1)
    # 卖出信号：当天最低价 < 昨天的 n_exit 天最低值
    data['exit_long'] = data['low'] < data['exit_low'].shift(1)

    return data


# 回测策略
# 回测策略
def backtest(data, initial_capital=100000, risk_per_trade=0.02, slippage=0.01, cost=0.001):
    capital = initial_capital
    position = 0.0  # 持仓数量初始化为浮点数
    capital_curve = []
    buy_price = None

    # 新增列初始化并指定数据类型
    data['buy_price'] = None
    data['sell_price'] = None
    data['position'] = 0.0  # 持仓数量为浮点数
    data['buy_amount'] = 0.0  # 买入金额为浮点数
    data['buy_quantity'] = 0.0  # 买入数量为浮点数
    data['sell_amount'] = 0.0  # 卖出金额为浮点数
    data['sell_quantity'] = 0.0  # 卖出数量为浮点数

    for i in range(len(data)):
        row = data.iloc[i]

        # 买入逻辑
        if row['long_signal'] and position == 0:
            buy_price = data['entry_high'].shift(1).iloc[i] * (1 + slippage)
            position = capital * risk_per_trade / buy_price  # 计算持仓数量
            buy_amount = position * buy_price  # 买入金额
            capital -= buy_amount  # 扣除买入资金
            capital -= buy_amount * cost  # 扣除交易成本
            data.loc[row.name, 'buy_price'] = float(buy_price)  # 显式转换为浮点数
            data.loc[row.name, 'buy_amount'] = float(buy_amount)  # 显式转换为浮点数
            data.loc[row.name, 'buy_quantity'] = float(position)  # 显式转换为浮点数

        # 卖出逻辑
        elif row['exit_long'] and position > 0:
            sell_price = data['exit_low'].shift(1).iloc[i] * (1 - slippage)
            sell_amount = position * sell_price  # 卖出金额
            capital += sell_amount  # 加回卖出资金
            capital -= sell_amount * cost  # 扣除交易成本
            data.loc[row.name, 'sell_price'] = float(sell_price)  # 显式转换为浮点数
            data.loc[row.name, 'sell_amount'] = float(sell_amount)  # 显式转换为浮点数
            data.loc[row.name, 'sell_quantity'] = float(position)  # 显式转换为浮点数
            position = 0.0  # 清空持仓，确保为浮点数
            buy_price = None

        # 更新每日资金曲线
        capital_curve.append(capital + position * row['close'])
        data.loc[row.name, 'position'] = float(position)  # 显式转换为浮点数

    data['capital_curve'] = capital_curve
    return data



# 可视化结果
# 可视化结果
# 数据归一化
def normalize_data(data, columns):
    """
    对指定的列进行 Min-Max 归一化。

    参数:
    - data: 输入的 DataFrame 数据
    - columns: 需要归一化的列名列表

    返回:
    - 归一化后的 DataFrame
    """
    for column in columns:
        min_value = data[column].min()
        max_value = data[column].max()
        data[column] = (data[column] - min_value) / (max_value - min_value)
    return data


# 可视化结果
def plot_results(data):
    """
    绘制归一化后的资金曲线和每日收盘价。

    参数:
    - data: 包含资金曲线和收盘价的数据集
    """
    # 对资金曲线和收盘价进行归一化
    data_normalized = normalize_data(data.copy(), columns=['capital_curve', 'close'])

    # 绘制归一化后的资金曲线和收盘价
    plt.figure(figsize=(12, 6))
    plt.plot(data_normalized['capital_curve'], label='Normalized Capital Curve', color='blue')
    plt.plot(data_normalized['close'], label='Normalized Close Price', color='orange', alpha=0.5)

    # 设置图表标题和标签
    plt.title('Normalized Turtle Strategy Backtest Result')
    plt.xlabel('Date')
    plt.ylabel('Normalized Value')
    plt.legend()

    # 显示图表
    plt.show()


# 主程序
if __name__ == '__main__':
    symbol = "600586"  # 股票代码


    data = load_data(symbol, start="20200901", end="20250122")
    # data = turtle_signals(data)
    # data = backtest(data, slippage=0.01, cost=0.001)  # 设置滑点和交易成本
    data = turtle_signals(data, n_entry=40, n_exit=20)
    data = backtest(data, initial_capital=100000, risk_per_trade=1, slippage=0.01, cost=0.001)
    data.to_excel("./data/turtle_backtest.xlsx")  # 保存结果
    plot_results(data)
