import akshare as ak
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # 或者使用 'Agg' 或 'Qt5Agg'
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体，确保系统中安装了该字体

# 设置负号正常显示
plt.rcParams['axes.unicode_minus'] = False

# 沪深300 2009-07-10
hushen300_df = ak.fund_open_fund_info_em(symbol="110020", indicator="累计净值走势")
# 黄金 2020-07-16
gold_df = ak.fund_open_fund_info_em(symbol="002611", indicator="累计净值走势")
# 国债 2016-09-26
guozhai_df = ak.fund_open_fund_info_em(symbol="003376", indicator="累计净值走势")
# 现金
cash_df = ak.fund_open_fund_info_em(symbol="070009", indicator="累计净值走势")

# 转换净值日期为日期格式，方便对齐时间
hushen300_df['净值日期'] = pd.to_datetime(hushen300_df['净值日期'])
gold_df['净值日期'] = pd.to_datetime(gold_df['净值日期'])
guozhai_df['净值日期'] = pd.to_datetime(guozhai_df['净值日期'])
cash_df['净值日期'] = pd.to_datetime(cash_df['净值日期'])

# 合并数据
merged_df = hushen300_df[['净值日期', '累计净值']].rename(columns={'累计净值': '沪深300'}).merge(
    gold_df[['净值日期', '累计净值']].rename(columns={'累计净值': '黄金'}), on='净值日期', how='inner'
).merge(
    guozhai_df[['净值日期', '累计净值']].rename(columns={'累计净值': '国债'}), on='净值日期', how='inner'
).merge(
    cash_df[['净值日期', '累计净值']].rename(columns={'累计净值': '现金'}), on='净值日期', how='inner'
)

# 获取回测的起始和结束日期
start_date = merged_df['净值日期'].iloc[0]
end_date = merged_df['净值日期'].iloc[-1]

# 初始净值设置
initial_weights = {'沪深300': 0.25, '黄金': 0.25, '国债': 0.25, '现金': 0.25}
merged_df[['沪深300', '黄金', '国债', '现金']] /= merged_df[['沪深300', '黄金', '国债', '现金']].iloc[0]  # 归一化净值

# 计算组合净值
merged_df['组合净值'] = (
    merged_df['沪深300'] * initial_weights['沪深300'] +
    merged_df['黄金'] * initial_weights['黄金'] +
    merged_df['国债'] * initial_weights['国债'] +
    merged_df['现金'] * initial_weights['现金']
)

# 计算现金部分的年化收益率作为无风险收益率
cash_annual_return = (merged_df['现金'].iloc[-1] / merged_df['现金'].iloc[0]) ** (252 / len(merged_df)) - 1

# 每年再平衡
def rebalance_portfolio(row, weights):
    total_value = sum(row[asset] * weights[asset] for asset in weights)
    for asset in weights:
        weights[asset] = weights[asset] * row[asset] / total_value
    return total_value

merged_df['组合净值'] = merged_df.apply(lambda row: rebalance_portfolio(row, initial_weights) if row.name % 252 == 0 else row['组合净值'], axis=1)

# 计算年化收益率
annual_return = (merged_df['组合净值'].iloc[-1] / merged_df['组合净值'].iloc[0]) ** (252 / len(merged_df)) - 1

# 计算最大回撤及起止日期
merged_df['累计最大值'] = merged_df['组合净值'].cummax()
merged_df['回撤'] = (merged_df['组合净值'] - merged_df['累计最大值']) / merged_df['累计最大值']
max_drawdown = merged_df['回撤'].min()

# 找到最大回撤的起止日期
end_date_max_drawdown = merged_df['净值日期'][merged_df['回撤'].idxmin()]
start_date_max_drawdown = merged_df['净值日期'][(merged_df['组合净值'].cummax()[:merged_df['回撤'].idxmin()]).idxmax()]

# 计算每日收益率
merged_df['每日收益率'] = merged_df['组合净值'].pct_change()

# 计算组合的年化波动率
annual_volatility = merged_df['每日收益率'].std() * (252 ** 0.5)

# 计算组合的年化超额收益率（使用现金部分的年化收益率作为无风险收益率）
annual_excess_return = annual_return - cash_annual_return

# 计算夏普比率
sharpe_ratio = annual_excess_return / annual_volatility

# 打印回测结果
print("回测起始日期:", start_date)
print("回测结束日期:", end_date)
print("年化收益率: {:.2%}".format(annual_return))
print("最大回撤: {:.2%}".format(max_drawdown))
print("最大回撤起始日期:", start_date_max_drawdown)
print("最大回撤结束日期:", end_date_max_drawdown)
print("现金部分年化收益率: {:.2%}".format(cash_annual_return))
print("夏普比率: {:.2f}".format(sharpe_ratio))

# 绘制净值曲线
plt.figure(figsize=(12, 6))
plt.plot(merged_df['净值日期'], merged_df['组合净值'], label='组合净值', color='blue')
plt.xlabel("日期")
plt.ylabel("组合净值")
plt.title("组合净值曲线")
plt.legend()
plt.grid(True)
plt.show()
