import akshare as ak
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # 或者使用 'Agg' 或 'Qt5Agg'
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体，确保系统中安装了该字体
plt.rcParams['axes.unicode_minus'] = False

# 获取数据
hushen300_df = ak.fund_open_fund_info_em(symbol="090010", indicator="累计净值走势")
gold_df = ak.fund_open_fund_info_em(symbol="002611", indicator="累计净值走势")

# 转换日期列为日期类型
hushen300_df['净值日期'] = pd.to_datetime(hushen300_df['净值日期'])
gold_df['净值日期'] = pd.to_datetime(gold_df['净值日期'])

# 设置日期为索引
hushen300_df.set_index('净值日期', inplace=True)
gold_df.set_index('净值日期', inplace=True)

# 提取累计净值列并重命名，便于合并
hushen300_df = hushen300_df[['累计净值']].rename(columns={'累计净值': '沪深300基金'})
gold_df = gold_df[['累计净值']].rename(columns={'累计净值': '黄金基金'})

# 合并数据，按日期对齐
merged_df = pd.merge(hushen300_df, gold_df, left_index=True, right_index=True, how='inner')

# 数据归一化（以初始值为基准）
normalized_df = merged_df / merged_df.iloc[0]

# 计算相关性
correlation = merged_df.corr().iloc[0, 1]  # 取相关矩阵的第一个非对角线值

# 打印结果
print(f"沪深300基金与黄金基金的相关性: {correlation:.4f}")

# 可视化
plt.figure(figsize=(10, 6))
plt.plot(normalized_df.index, normalized_df['沪深300基金'], label='红利基金')
plt.plot(normalized_df.index, normalized_df['黄金基金'], label='黄金基金')
plt.title('基金累计净值走势（归一化）')
plt.xlabel('日期')
plt.ylabel('累计净值（归一化）')
plt.legend()
plt.grid()
plt.show()
