import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd
# 设置编码格式，防止中文乱码
from utils.file_tool import save_dataframe_to_excel

plt.rcParams['font.sans-serif'] = ['SimHei']
# df_etf = ak.fund_etf_hist_em(symbol="510300", period="daily", start_date="20211229", end_date="20230822", adjust="qfq")
df_etf = ak.fund_etf_hist_em(symbol="510300", period="daily",  adjust="qfq")
df_etf['日期'] = pd.to_datetime(df_etf['日期'])

# 创建图表
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制收盘价曲线图在第一个纵坐标轴
ax1.plot(df_etf['日期'], df_etf['收盘'], linestyle='-', color='b', label='收盘价')
ax1.set_xlabel('日期')
ax1.set_ylabel('收盘价', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_title('收盘价和成交额趋势')

# 创建第二个纵坐标轴，共享横坐标
ax2 = ax1.twinx()
ax2.bar(df_etf['日期'], df_etf['成交额'], color='g', alpha=0.5, label='成交额')
ax2.set_ylabel('成交额', color='g')
ax2.tick_params(axis='y', labelcolor='g')

# 找到2019-01-02和2022-10-31这两个日期的收盘价
close_20190102 = df_etf[df_etf['日期'] == '2019-01-02']['收盘'].values[0]
close_20221031 = df_etf[df_etf['日期'] == '2022-10-31']['收盘'].values[0]

# 找到最新的日期的收盘价
close_latest = df_etf['收盘'].iloc[-1]

# 获取x轴范围
x_range = df_etf['日期'].iloc[-1] - df_etf['日期'].iloc[0]

# 计算直线的斜率和截距
slope = (close_20221031 - close_20190102) / (pd.Timestamp('2022-10-31') - pd.Timestamp('2019-01-02')).days
intercept = close_20190102 - slope * (pd.Timestamp('2019-01-02') - df_etf['日期'].iloc[0]).days

# 绘制连接2019-01-02和2022-10-31这两个日期的直线，并延伸到最新日期
ax1.plot(df_etf['日期'], slope * (df_etf['日期'] - df_etf['日期'].iloc[0]).dt.days + intercept,
         color='r', linestyle='--', label='直线连接')

# 设置图例
lines, labels = ax1.get_legend_handles_labels()
bars, bar_labels = ax2.get_legend_handles_labels()
ax2.legend(lines + bars, labels + bar_labels, loc='upper left')

plt.xticks(rotation=45)
plt.tight_layout()
# 在起始位置和结束位置添加日期标注
start_annotation = df_etf.iloc[0]['日期'].strftime('%Y-%m-%d')
end_annotation = df_etf.iloc[-1]['日期'].strftime('%Y-%m-%d')

ax1.annotate(f'起始日期: {start_annotation}',
             xy=(df_etf.iloc[0]['日期'], df_etf.iloc[0]['收盘']),
             xytext=(10, 30), textcoords='offset points',
             arrowprops=dict(arrowstyle='->', color='black'))

ax1.annotate(f'结束日期: {end_annotation}',
             xy=(df_etf.iloc[-1]['日期'], df_etf.iloc[-1]['收盘']),
             xytext=(-110, -50), textcoords='offset points',
             arrowprops=dict(arrowstyle='->', color='black'))
# 保存图表为临时文件
chart_path3 = 'chart_temp3.png'
plt.savefig(chart_path3)
plt.close()