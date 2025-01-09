import pymysql
import pandas as pd
import time
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

# 连接MySQL并获取基金代码
def get_fund_codes():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 查询所有基金代码
    cursor.execute("SELECT DISTINCT fund_code FROM fund_net_value")
    fund_codes = cursor.fetchall()

    conn.close()
    return [fund_code[0] for fund_code in fund_codes]
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
import pandas as pd


def calculate_annualized_return(df, years=None):
    """
    计算年化收益率。
    如果指定 years 参数，则计算近 years 年的数据，否则计算全部数据。
    """
    if df.empty:
        return None

    # 如果传入 years 参数，确定起始日期
    if years:
        end_date = df.index[-1]  # 数据的最后日期
        start_date = end_date - pd.DateOffset(years=years)  # 计算起始日期

        # 筛选近 years 年的数据
        df = df[df.index >= start_date]
        if df.empty:  # 如果筛选后没有数据
            return None

    # 获取起始和结束净值
    start_value = float(df['cumulative_net_value'].iloc[0])
    end_value = float(df['cumulative_net_value'].iloc[-1])

    # 确定实际的时间跨度（年）
    period_years = (df.index[-1] - df.index[0]).days / 365

    # 防止除以零
    if start_value == 0 or period_years == 0:
        return None

    # 计算年化收益率
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

    # 找到最大回撤的结束时间（最低点）
    drawdown_end_date = df['drawdown'].idxmin()

    # 找到最大回撤的起始时间，即最大值发生的时间点
    drawdown_start_date = df[df['rolling_max'] == df.loc[drawdown_end_date, 'rolling_max']].index[0]

    # 计算回撤持续时间
    drawdown_duration = (drawdown_end_date - drawdown_start_date).days

    # 计算净值修复天数
    recovery_date = df[(df.index > drawdown_end_date) & (df['cumulative_net_value'] >= df.loc[drawdown_start_date, 'rolling_max'])].index
    if not recovery_date.empty:
        recovery_days = (recovery_date[0] - drawdown_end_date).days
    else:
        recovery_days = None  # 未恢复到历史最高点

    return max_drawdown, drawdown_start_date, drawdown_end_date, drawdown_duration, recovery_days



# 计算年化波动率
def calculate_annualized_volatility(df):
    df['daily_return'] = df['cumulative_net_value'].pct_change(fill_method=None)
    df['daily_return'].dropna(inplace=True)

    # 将 daily_return 列转换为 float 类型，确保计算时没有类型冲突
    df['daily_return'] = df['daily_return'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

    daily_volatility = df['daily_return'].std()
    annualized_volatility = daily_volatility * (252 ** 0.5)  # 假设每年252个交易日
    return annualized_volatility


# 计算夏普率
def calculate_sharpe_ratio(annualized_return, annualized_volatility, risk_free_rate=0):
    if annualized_return is None or annualized_volatility == 0:
        return None  # 或者返回一个默认值，例如 0
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
    return sharpe_ratio



# 计算卡玛率
def calculate_calmar_ratio(annualized_return, max_drawdown):
    # 将 max_drawdown 转换为 float，避免与 float 类型的 annualized_return 冲突
    calmar_ratio = annualized_return / -float(max_drawdown)
    return calmar_ratio


# 计算季度胜率
def calculate_quarterly_win_rate(df):
    # 为每一行数据分配季度
    df['quarter'] = df.index.to_period('Q')

    # 计算每个季度的收益率：当前季度的最后一日净值与首日净值的变化百分比
    quarterly_return = df.groupby('quarter')['cumulative_net_value'].apply(lambda x: x.iloc[-1] / x.iloc[0] - 1)

    # 计算正收益季度数
    positive_quarters = (quarterly_return > 0).sum()

    # 计算总季度数
    total_quarters = len(quarterly_return)

    # 计算季度胜率
    quarterly_win_rate = positive_quarters / total_quarters
    return quarterly_win_rate


def calculate_win_rate(df):
    # 计算每日的收益率
    df['daily_return'] = df['cumulative_net_value'].pct_change(fill_method=None)

    # 计算上涨天数（每日收益率大于0的天数）
    win_days = df[df['daily_return'] > 0].shape[0]

    # 计算总交易天数
    total_days = df.shape[0]

    # 计算胜率
    win_rate = win_days / total_days
    return win_rate

def calculate_new_high_days_ratio(df):
    """
    计算创新高天数占总天数的比例。

    参数:
    df: pd.DataFrame - 必须包含 'cumulative_net_value' 列，且索引为日期时间类型。

    返回:
    tuple - (创新高天数, 总天数, 创新高天数占比)
    """
    # 计算每个日期前的累计最大值
    df['rolling_max'] = df['cumulative_net_value'].cummax()

    # 判断是否为创新高
    df['is_new_high'] = df['cumulative_net_value'] >= df['rolling_max']

    # 计算创新高天数和总天数
    new_high_days = df['is_new_high'].sum()  # 创新高天数
    total_days = len(df)  # 总天数

    # 计算创新高天数占比
    new_high_ratio = new_high_days / total_days

    return new_high_days, total_days, new_high_ratio

def calculate_avg_gain_loss(df):
    """
    计算平均每次亏损的幅度和盈利的幅度。

    参数:
    df: pd.DataFrame - 必须包含 'cumulative_net_value' 列，且索引为日期时间类型。

    返回:
    tuple - (平均亏损幅度, 平均盈利幅度)
    """
    # 计算每日收益率
    df['daily_return'] = df['cumulative_net_value'].pct_change(fill_method=None)

    # 筛选出亏损和盈利的收益率
    loss_returns = df['daily_return'][df['daily_return'] < 0]
    gain_returns = df['daily_return'][df['daily_return'] > 0]

    # 计算平均亏损幅度和平均盈利幅度
    avg_loss = loss_returns.mean() * 100 if not loss_returns.empty else 0
    avg_gain = gain_returns.mean() * 100 if not gain_returns.empty else 0

    return avg_loss, avg_gain

# 主程序
# 计算并保存每个基金的指标
# 计算并保存每个基金的指标
def calculate_and_save_results(fund_codes):
    results = []  # 存储所有基金的结果
    errors = []   # 存储出错的基金代码和错误信息

    for fund_code in fund_codes:
        try:
            print(f"processing fund code {fund_code}")
            df = get_fund_data(fund_code)

            # 计算各项指标
            annualized_return = calculate_annualized_return(df)
            annualized_return1 = calculate_annualized_return(df, 1)
            annualized_return3 = calculate_annualized_return(df, 3)
            annualized_return5 = calculate_annualized_return(df, 5)
            max_drawdown, start_date, end_date, duration, recovery_days = calculate_max_drawdown(df)
            annualized_volatility = calculate_annualized_volatility(df)
            sharpe_ratio = calculate_sharpe_ratio(annualized_return, annualized_volatility)
            calmar_ratio = calculate_calmar_ratio(annualized_return, max_drawdown)
            quarterly_win_rate = calculate_quarterly_win_rate(df)
            win_rate = calculate_win_rate(df)
            avg_loss, avg_gain = calculate_avg_gain_loss(df)
            new_high_days, total_days, new_high_ratio = calculate_new_high_days_ratio(df)
            # 存储每个基金的结果
            results.append({
                '基金代码': fund_code,
                '年化收益率': annualized_return,
                '近1年年化收益率': annualized_return1,
                '近3年年化收益率': annualized_return3,
                '近5年年化收益率': annualized_return5,
                '最大回撤': max_drawdown,
                '回撤开始日期': start_date,
                '回撤结束日期': end_date,
                '回撤持续天数': duration,
                '净值恢复所需天数': recovery_days if recovery_days is not None else '尚未恢复',
                '年化波动率': annualized_volatility,
                '夏普率': sharpe_ratio,
                '卡玛率': calmar_ratio,
                '季度胜率': quarterly_win_rate,
                '胜率': win_rate,
                '平均亏损幅度': avg_loss,
                '平均盈利幅度': avg_gain,
                '创新高天数占比': new_high_ratio
            })

        except Exception as e:
            # 如果某个基金代码出错，记录错误信息
            print(f"Error processing fund code {fund_code}: {e}")
            errors.append({'代码': fund_code, '错误信息': str(e)})

    # 将结果存储到 DataFrame
    df_results = pd.DataFrame(results)
    df_results.to_excel('./data/dbFundPerformance.xlsx', index=False)

    # 如果有错误，将错误信息保存到一个单独的 Excel 文件
    # if errors:
    #     df_errors = pd.DataFrame(errors)
    #     df_errors.to_excel('./data/fund_errors.xlsx', index=False)
    #     print("Errors occurred. Details saved in 'fund_errors.xlsx'.")

# 主函数，遍历基金代码并执行计算
def main():
    start_time = time.time()  # 程序开始时间

    fund_codes = get_fund_codes()  # 获取基金代码列表
    calculate_and_save_results(fund_codes)  # 计算并保存结果
    # calculate_and_save_results(['002117'])  # 计算并保存结果

    end_time = time.time()  # 程序结束时间

    # 打印程序执行时间
    elapsed_time = end_time - start_time
    print(f"程序执行完毕，总耗时：{elapsed_time:.2f} 秒")  # 精确到小数点后2位

# 示例调用
if __name__ == '__main__':
    main()