import akshare as ak

df = ak.stock_ebs_lg()


# 初始化变量
current_streak_start = None
current_streak_length = 0

# 遍历数据并计算每段时间的持续天数
for index, row in df.iterrows():
    if row['股债利差'] > row['股债利差均线']:
        if current_streak_start is None:
            current_streak_start = row['日期']
        current_streak_length += 1
    else:
        if current_streak_length > 1:
            print("起始日期:", current_streak_start)
            print("结束日期:", df.iloc[index - 1]['日期'])
            print("持续天数:", current_streak_length)
        current_streak_start = None
        current_streak_length = 0

# 处理最后一段时间的情况
if current_streak_length > 1:
    print("起始日期:", current_streak_start)
    print("结束日期:", df.iloc[-1]['日期'])
    print("持续天数:", current_streak_length)
