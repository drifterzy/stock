import pandas as pd


# 读取原始的回测数据
def load_backtest_results(file_path):
    """
    读取回测结果文件。

    参数:
    - file_path: 原始回测结果的文件路径

    返回:
    - DataFrame: 包含回测结果的数据
    """
    data = pd.read_excel(file_path)
    return data


# 计算交易统计信息，包括最大回撤和年化收益
def calculate_trade_statistics(data, initial_capital=100000):
    """
    计算交易统计信息：总交易次数、盈利交易次数、亏损交易次数、平均盈利、平均亏损、最大回撤和年化收益。

    参数:
    - data: 回测结果数据
    - initial_capital: 初始资金（默认为100000）

    返回:
    - dict: 交易统计信息
    """
    trades = []  # 存储交易信息（买入日期, 卖出日期, 盈利/亏损）
    profit_trades = 0  # 盈利交易次数
    loss_trades = 0  # 亏损交易次数
    total_profit = 0  # 总盈利
    total_loss = 0  # 总亏损
    position = 0  # 当前持仓状态
    capital = initial_capital  # 初始化资金为初始资金

    # 记录未平仓的买入信号
    buy_signal = None
    buy_price = None
    buy_quantity = 0

    capital_curve = [capital]  # 初始资金曲线，起始点为初始资金

    start_date = None  # 回测开始日期
    end_date = None  # 回测结束日期

    for i in range(len(data)):
        row = data.iloc[i]

        # 记录回测开始和结束的日期
        if i == 0:
            start_date = row['date']
        if i == len(data) - 1:
            end_date = row['date']

        # 检查买入信号
        if row['long_signal'] and position == 0:  # 如果没有持仓且出现买入信号
            buy_signal = row.name
            buy_price = row['buy_price']  # 使用买入价格（假设买入价格是前一天的最高价）
            buy_quantity = row['buy_quantity']  # 假设买入数量已知
            position = buy_quantity  # 更新持仓状态
            continue  # 跳过后续步骤

        # 检查卖出信号
        if row['exit_long'] and position > 0:  # 如果有持仓且出现卖出信号
            sell_price = row['sell_price']  # 使用卖出价格
            sell_quantity = position
            profit = (sell_price - buy_price) * sell_quantity - (buy_price * 0.001 + sell_price * 0.001)  # 考虑交易成本

            trades.append({
                'buy_date': data.loc[buy_signal, 'date'],
                'sell_date': row['date'],
                'buy_price': buy_price,
                'sell_price': sell_price,
                'profit': profit
            })

            if profit > 0:
                profit_trades += 1
                total_profit += profit
            else:
                loss_trades += 1
                total_loss += profit

            # 更新资金
            capital += profit  # 将盈利或亏损加到总资金中
            capital_curve.append(capital)  # 将当前资金加入资金曲线

            # 重置持仓状态
            position = 0
            buy_signal = None
            buy_price = None
            buy_quantity = 0

    # 计算最大回撤
    capital_curve = pd.Series(capital_curve)  # 转换为 pandas Series 以便计算
    peak = capital_curve.cummax()  # 计算每时点的历史最大资金值
    drawdown = (capital_curve - peak) / peak  # 计算回撤
    max_drawdown = drawdown.min()  # 最大回撤

    # 计算年化收益
    total_return = (capital - initial_capital) / initial_capital  # 总收益率
    # 计算回测期的年数
    duration_years = (end_date - start_date).days / 365.0
    annualized_return = (1 + total_return) ** (1 / duration_years) - 1 if duration_years > 0 else 0

    # 计算平均盈利和平均亏损
    avg_profit = total_profit / profit_trades if profit_trades > 0 else 0
    avg_loss = total_loss / loss_trades if loss_trades > 0 else 0

    return {
        'total_trades': len(trades),
        'profit_trades': profit_trades,
        'loss_trades': loss_trades,
        'avg_profit': avg_profit,
        'avg_loss': avg_loss,
        'max_drawdown': max_drawdown,
        'annualized_return': annualized_return,
        'trades': trades
    }


# 保存交易统计信息到新的文件
def save_trade_statistics(stats, output_file_path):
    """
    保存交易统计信息到 Excel 文件。

    参数:
    - stats: 交易统计信息
    - output_file_path: 输出文件路径
    """
    # 创建一个包含统计信息的 DataFrame
    summary_df = pd.DataFrame({
        'Total Trades': [stats['total_trades']],
        'Profit Trades': [stats['profit_trades']],
        'Loss Trades': [stats['loss_trades']],
        'Average Profit': [stats['avg_profit']],
        'Average Loss': [stats['avg_loss']],
        'Max Drawdown': [stats['max_drawdown']],
        'Annualized Return': [stats['annualized_return']]
    })

    trades_df = pd.DataFrame(stats['trades'])  # 交易详细信息

    # 将统计信息和交易数据保存到 Excel 文件
    with pd.ExcelWriter(output_file_path) as writer:
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        trades_df.to_excel(writer, sheet_name='Trades', index=False)


# 主程序
if __name__ == '__main__':
    input_file = './data/turtle_backtest.xlsx'  # 输入文件路径
    output_file = './data/turtle_trade_analysis.xlsx'  # 输出文件路径

    # 读取原始回测结果
    data = load_backtest_results(input_file)

    # 计算交易统计信息
    stats = calculate_trade_statistics(data)

    # 保存分析结果到新的 Excel 文件
    save_trade_statistics(stats, output_file)

    print(f"交易统计结果已保存到: {output_file}")
