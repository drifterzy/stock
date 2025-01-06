import pymysql
import pandas as pd
from decimal import Decimal
from datetime import datetime
# 数据库连接配置
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}

# 连接MySQL
def get_fund_data(fund_code):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 查询基金数据
    cursor.execute("""
        SELECT fund_code, net_value_date, cumulative_net_value 
        FROM fund_net_value 
        WHERE fund_code = %s
        ORDER BY net_value_date
    """, (fund_code,))

    data = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(data, columns=['fund_code', 'net_value_date', 'cumulative_net_value'])
    df['net_value_date'] = pd.to_datetime(df['net_value_date'])
    df.set_index('net_value_date', inplace=True)

    # 将累计净值列转换为 float 类型，以避免 decimal 和 float 类型冲突
    df['cumulative_net_value'] = df['cumulative_net_value'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

    return df


# 计算年化收益率
def calculate_annualized_return(df):
    start_value = float(df['cumulative_net_value'].iloc[0])  # 转换为float
    end_value = float(df['cumulative_net_value'].iloc[-1])  # 转换为float
    period_years = (df.index[-1] - df.index[0]).days / 365

    annualized_return = (end_value / start_value) ** (1 / period_years) - 1
    return annualized_return


# 计算最大回撤
def calculate_max_drawdown(df):
    # 计算每个日期前的累计最大值
    df['rolling_max'] = df['cumulative_net_value'].cummax()

    # 计算回撤：当前净值与历史最大净值的差值 / 历史最大净值
    df['drawdown'] = (df['cumulative_net_value'] - df['rolling_max']) / df['rolling_max']

    # 找到最大回撤的最小值
    max_drawdown = df['drawdown'].min()

    # 找到最大回撤的起始时间和结束时间
    drawdown_end_date = df['drawdown'].idxmin()  # 最大回撤的结束时间（最低点）

    # 获取最大回撤的起始时间，即最大值发生的时间点
    drawdown_start_date = df[df['rolling_max'] == df.loc[drawdown_end_date, 'rolling_max']].index[0]

    return max_drawdown, drawdown_start_date, drawdown_end_date


# 计算年化波动率
def calculate_annualized_volatility(df):
    df['daily_return'] = df['cumulative_net_value'].pct_change()
    df['daily_return'].dropna(inplace=True)

    # 将 daily_return 列转换为 float 类型，确保计算时没有类型冲突
    df['daily_return'] = df['daily_return'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

    daily_volatility = df['daily_return'].std()
    annualized_volatility = daily_volatility * (252 ** 0.5)  # 假设每年252个交易日
    return annualized_volatility


# 计算夏普率
def calculate_sharpe_ratio(annualized_return, annualized_volatility, risk_free_rate=0):
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
    return sharpe_ratio


# 计算卡玛率
def calculate_calmar_ratio(annualized_return, max_drawdown):
    # 将 max_drawdown 转换为 float，避免与 float 类型的 annualized_return 冲突
    calmar_ratio = annualized_return / -float(max_drawdown)
    return calmar_ratio


# 计算季度胜率
def calculate_quarterly_win_rate(df):
    df['quarter'] = df.index.to_period('Q')
    df['quarterly_return'] = df['cumulative_net_value'].pct_change()

    quarterly_win_rate = (
                df[df['quarterly_return'] > 0].groupby('quarter').size() / df.groupby('quarter').size()).mean()
    return quarterly_win_rate


# 主程序
def main(fund_code):
    df = get_fund_data(fund_code)

    annualized_return = calculate_annualized_return(df)
    max_drawdown, drawdown_start_date, drawdown_end_date = calculate_max_drawdown(df)
    annualized_volatility = calculate_annualized_volatility(df)
    sharpe_ratio = calculate_sharpe_ratio(annualized_return, annualized_volatility)
    calmar_ratio = calculate_calmar_ratio(annualized_return, max_drawdown)
    quarterly_win_rate = calculate_quarterly_win_rate(df)

    # 打印结果
    print(f"基金代码: {fund_code}")
    print(f"年化收益率: {annualized_return:.4f}")
    print(f"最大回撤: {max_drawdown:.4f}")
    print(f"回撤起始时间: {drawdown_start_date}")
    print(f"回撤结束时间: {drawdown_end_date}")
    print(f"年化波动率: {annualized_volatility:.4f}")
    print(f"夏普率: {sharpe_ratio:.4f}")
    print(f"卡玛率: {calmar_ratio:.4f}")
    print(f"季度胜率: {quarterly_win_rate:.4f}")


# 示例调用
if __name__ == '__main__':
    fund_code = '000001'  # 替换为你需要查询的基金代码
    main(fund_code)
