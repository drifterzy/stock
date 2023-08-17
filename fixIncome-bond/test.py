import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors  # 导入 mplcursors 库
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
index_zh_a_hist_df = ak.index_zh_a_hist(symbol="000016", period="daily", start_date="20230101", end_date="20230816")
index_zh_a_hist_df2 = ak.index_zh_a_hist(symbol="399300", period="daily", start_date="20230101", end_date="20230816")
index_zh_a_hist_df3 = ak.index_zh_a_hist(symbol="000905", period="daily", start_date="20230101", end_date="20230816")
index_zh_a_hist_df4 = ak.index_zh_a_hist(symbol="000852", period="daily", start_date="20230101", end_date="20230816")
# 假设 index_zh_a_hist_df 和 index_zh_a_hist_df2 是你的两个 DataFrames
# 可能需要将日期列转换为日期类型
# 假设 index_zh_a_hist_df、index_zh_a_hist_df2、index_zh_a_hist_df3 和 index_zh_a_hist_df4 是你的四个 DataFrames
# 可能需要将日期列转换为日期类型
index_zh_a_hist_df['日期'] = pd.to_datetime(index_zh_a_hist_df['日期'])
index_zh_a_hist_df2['日期'] = pd.to_datetime(index_zh_a_hist_df2['日期'])
index_zh_a_hist_df3['日期'] = pd.to_datetime(index_zh_a_hist_df3['日期'])
index_zh_a_hist_df4['日期'] = pd.to_datetime(index_zh_a_hist_df4['日期'])

# 将共同起点的收盘价作为基准
base_price1 = index_zh_a_hist_df['收盘'].iloc[0]
base_price2 = index_zh_a_hist_df2['收盘'].iloc[0]
base_price3 = index_zh_a_hist_df3['收盘'].iloc[0]
base_price4 = index_zh_a_hist_df4['收盘'].iloc[0]

# 计算每只股票的相对初始收盘价
index_zh_a_hist_df['相对收盘价'] = index_zh_a_hist_df['收盘'] / base_price1
index_zh_a_hist_df2['相对收盘价'] = index_zh_a_hist_df2['收盘'] / base_price2
index_zh_a_hist_df3['相对收盘价'] = index_zh_a_hist_df3['收盘'] / base_price3
index_zh_a_hist_df4['相对收盘价'] = index_zh_a_hist_df4['收盘'] / base_price4

# 调整绘图粗细和标签显示
fig, ax = plt.subplots(figsize=(10, 6))
lines1, = ax.plot(index_zh_a_hist_df['日期'], index_zh_a_hist_df['相对收盘价'], marker='o', markersize=2, linestyle='-', color='b', label='股票1 相对收盘价')
lines2, = ax.plot(index_zh_a_hist_df2['日期'], index_zh_a_hist_df2['相对收盘价'], marker='x', markersize=2, linestyle='-', color='g', label='股票2 相对收盘价')
lines3, = ax.plot(index_zh_a_hist_df3['日期'], index_zh_a_hist_df3['相对收盘价'], marker='s', markersize=2, linestyle='-', color='r', label='股票3 相对收盘价')
lines4, = ax.plot(index_zh_a_hist_df4['日期'], index_zh_a_hist_df4['相对收盘价'], marker='^', markersize=2, linestyle='-', color='purple', label='股票4 相对收盘价')
ax.set_title('多只股票相对收盘价曲线图')
ax.set_xlabel('日期')
ax.set_ylabel('相对收盘价')
ax.grid(True)
ax.set_xticks(index_zh_a_hist_df['日期'][::365])
ax.set_xticklabels(index_zh_a_hist_df['日期'].dt.year[::365])  # 每年显示一个标签

# 添加鼠标悬停显示数值功能
mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f"日期: {sel.target[0]:%Y-%m-%d}\n相对收盘价: {sel.target[1]:.2f}"))

# 添加图例
ax.legend()

# 显示图像
plt.tight_layout()
plt.show()