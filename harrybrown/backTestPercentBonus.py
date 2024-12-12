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

# 获取数据
hushen300_df = ak.fund_open_fund_info_em(symbol="090010", indicator="累计净值走势")
gold_df = ak.fund_open_fund_info_em(symbol="002611", indicator="累计净值走势")
guozhai_df = ak.fund_open_fund_info_em(symbol="003376", indicator="累计净值走势")
cash_df = ak.fund_open_fund_info_em(symbol="070009", indicator="累计净值走势")

# 转换净值日期为日期格式
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

# 初始净值归一化和初始权重
initial_weights = {'沪深300': 0.25, '黄金': 0.25, '国债': 0.25, '现金': 0.25}
merged_df[['沪深300', '黄金', '国债', '现金']] /= merged_df[['沪深300', '黄金', '国债', '现金']].iloc[0]

# 动态权重调整逻辑
def rebalance_portfolio_if_needed(row, weights):
    total_value = sum(row[asset] * weights[asset] for asset in weights)
    weights_dynamic = {asset: (row[asset] * weights[asset]) / total_value for asset in weights}

    # 检查是否触发再平衡条件
    if any(w > 0.35 or w < 0.15 for w in weights_dynamic.values()):
        return sum(row[asset] * initial_weights[asset] for asset in initial_weights), initial_weights.copy()

    return total_value, weights

# 初始化组合净值和动态权重
portfolio_value = []
current_weights = initial_weights.copy()

for i, row in merged_df.iterrows():
    value, current_weights = rebalance_portfolio_if_needed(row, current_weights)
    portfolio_value.append(value)

merged_df['组合净值'] = portfolio_value

# 计算年化收益率
annual_return = (merged_df['组合净值'].iloc[-1] / merged_df['组合净值'].iloc[0]) ** (252 / len(merged_df)) - 1

# 计算现金部分的年化收益率作为无风险收益率
cash_annual_return = (merged_df['现金'].iloc[-1] / merged_df['现金'].iloc[0]) ** (252 / len(merged_df)) - 1

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
print("回测起始日期:", merged_df['净值日期'].iloc[0])
print("回测结束日期:", merged_df['净值日期'].iloc[-1])
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
