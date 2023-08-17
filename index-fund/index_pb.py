import akshare as ak
import matplotlib.pyplot as plt
from utils.file_tool import save_dataframe_to_excel

stock_a_all_pb_df = ak.stock_a_all_pb()

# 提取 middlePB 和 close 列数据
dates = stock_a_all_pb_df['date']
middlePB = stock_a_all_pb_df['middlePB']
close = stock_a_all_pb_df['close']

# 创建折线图
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制 middlePB 曲线，使用左侧纵轴
ax1.plot(dates, middlePB, marker='o', markersize=1, linestyle='-', color='b', label='middlePB')
ax1.set_xlabel('Date')
ax1.set_ylabel('middlePB', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True)
ax1.legend(loc='upper left')

# 创建右侧纵轴，用于绘制 close 曲线
ax2 = ax1.twinx()
ax2.plot(dates, close, marker='x', markersize=1,linestyle='-', color='g', label='close')
ax2.set_ylabel('close', color='g')
ax2.tick_params(axis='y', labelcolor='g')
ax2.legend(loc='upper right')

# 设置 x 轴日期显示格式
ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())

# 自动旋转 x 轴日期标签
plt.gcf().autofmt_xdate()

# 设置图标题
plt.title('middlePB vs close')

# 显示图像
plt.tight_layout()
plt.show()