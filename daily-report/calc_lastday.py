import pandas as pd
import akshare as ak
df = ak.stock_ebs_lg()


# 初始化变量
current_streak_start = None
current_streak_length = 0
yearly_streaks = {}

# 遍历数据并计算每段时间的持续天数
for index, row in df.iterrows():
    year = pd.to_datetime(row['日期']).year  # 提取年份部分
    if row['股债利差'] > row['股债利差均线']:
        if current_streak_start is None:
            current_streak_start = row['日期']
        current_streak_length += 1
    else:
        if current_streak_length > 1:
            # 更新年份统计
            if year not in yearly_streaks:
                yearly_streaks[year] = 0
            yearly_streaks[year] += min(current_streak_length, 365)

        current_streak_start = None
        current_streak_length = 0

# 处理最后一段时间的情况
if current_streak_length > 1:
    # 更新年份统计
    year = pd.to_datetime(current_streak_start).year
    if year not in yearly_streaks:
        yearly_streaks[year] = 0
    yearly_streaks[year] += min(current_streak_length, 365)

# 输出每年股债利差大于股债利差均线的总天数
for year in sorted(yearly_streaks.keys()):
    days = yearly_streaks[year]
    print(f"{year}年股债利差大于股债利差均线的总天数: {days} 天")
