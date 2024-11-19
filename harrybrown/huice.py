import pandas as pd

# 假设hushen300_df, gold_df, 和 guozhai_df已经包含数据
# 转换净值日期为日期格式，方便对齐时间
hushen300_df['净值日期'] = pd.to_datetime(hushen300_df['净值日期'])
gold_df['净值日期'] = pd.to_datetime(gold_df['净值日期'])
guozhai_df['净值日期'] = pd.to_datetime(guozhai_df['净值日期'])

# 合并数据
merged_df = hushen300_df[['净值日期', '单位净值']].rename(columns={'单位净值': '沪深300'}).merge(
    gold_df[['净值日期', '单位净值']].rename(columns={'单位净值': '黄金'}), on='净值日期', how='inner'
).merge(
    guozhai_df[['净值日期', '单位净值']].rename(columns={'单位净值': '国债'}), on='净值日期', how='inner'
)

# 初始净值设置
initial_weights = {'沪深300': 0.25, '黄金': 0.25, '国债': 0.25, '现金': 0.25}
merged_df[['沪深300', '黄金', '国债']] /= merged_df[['沪深300', '黄金', '国债']].iloc[0]  # 归一化净值
merged_df['现金'] = 1.0  # 假设现金保持1.0净值

# 计算组合净值
merged_df['组合净值'] = (
    merged_df['沪深300'] * initial_weights['沪深300'] +
    merged_df['黄金'] * initial_weights['黄金'] +
    merged_df['国债'] * initial_weights['国债'] +
    merged_df['现金'] * initial_weights['现金']
)

# 每年再平衡
def rebalance_portfolio(row, weights):
    total_value = sum(row[asset] * weights[asset] for asset in weights)
    for asset in weights:
        weights[asset] = weights[asset] * row[asset] / total_value
    return total_value

merged_df['组合净值'] = merged_df.apply(lambda row: rebalance_portfolio(row, initial_weights) if row.name % 252 == 0 else row['组合净值'], axis=1)

# 计算年化收益率和最大回撤
annual_return = (merged_df['组合净值'].iloc[-1] / merged_df['组合净值'].iloc[0]) ** (252 / len(merged_df)) - 1
max_drawdown = ((merged_df['组合净值'].cummax() - merged_df['组合净值']) / merged_df['组合净值'].cummax()).max()

print("年化收益率:", annual_return)
print("最大回撤:", max_drawdown)
