import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
# 设置编码格式，防止中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
# 获取股债利差值
df = ak.stock_ebs_lg()
# 将日期列转换为日期时间类型
df['日期'] = pd.to_datetime(df['日期'])
# 获取最新一天的数据
latest_data = df.iloc[-1]
# 提取最新一天的股债利差值、股债利差均值和它们之间的差值
latest_date = latest_data['日期']
latest_ebs = latest_data['股债利差']
latest_ebs_avg = latest_data['股债利差均线']
difference = latest_ebs - latest_ebs_avg
# 将数据存储为字符串
text = f"日期：{latest_date.strftime('%Y-%m-%d')}，股债利差值：{latest_ebs:.4f}，股债利差均值：{latest_ebs_avg:.4f}，差值：{difference:.4f}"

# 绘制图表
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制沪深300指数
ax1.plot(df['日期'], df['沪深300指数'], color='r', label='沪深300指数')
ax1.set_xlabel('日期')
ax1.set_ylabel('沪深300指数', color='r')
ax1.tick_params(axis='y', labelcolor='r')
ax1.legend(loc='upper left')

# 创建第二个坐标轴，用于绘制股债利差和股债利差均线
ax2 = ax1.twinx()
ax2.plot(df['日期'], df['股债利差'], color='b', label='股债利差',linewidth=0.2)
ax2.plot(df['日期'], df['股债利差均线'], color='g', label='股债利差均线',alpha=0.2)
ax2.set_ylabel('股债利差', color='b')
ax2.tick_params(axis='y', labelcolor='b')
ax2.legend(loc='upper right')

plt.title('股债利差与沪深300指数趋势')
# 在起始位置和结束位置添加日期标注
start_annotation = df.iloc[0]['日期'].strftime('%Y-%m-%d')
end_annotation = df.iloc[-1]['日期'].strftime('%Y-%m-%d')

ax1.annotate(f'起始日期: {start_annotation}',
             xy=(df.iloc[0]['日期'], df.iloc[0]['沪深300指数']),
             xytext=(10, 30), textcoords='offset points',
             arrowprops=dict(arrowstyle='->', color='black'))

ax1.annotate(f'结束日期: {end_annotation}',
             xy=(df.iloc[-1]['日期'], df.iloc[-1]['沪深300指数']),
             xytext=(-110, -50), textcoords='offset points',
             arrowprops=dict(arrowstyle='->', color='black'))

# 保存图表为临时文件
chart_path1 = 'chart_temp1.png'
plt.savefig(chart_path1)
plt.close()








start_date = pd.to_datetime('2021-12-29')
df = df[df['日期'] >= start_date]
# 绘制图表
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制沪深300指数
ax1.plot(df['日期'], df['沪深300指数'], color='r', label='沪深300指数')
ax1.set_xlabel('日期')
ax1.set_ylabel('沪深300指数', color='r')
ax1.tick_params(axis='y', labelcolor='r')
ax1.legend(loc='upper left')

# 创建第二个坐标轴，用于绘制股债利差和股债利差均线
ax2 = ax1.twinx()
ax2.plot(df['日期'], df['股债利差'], color='b', label='股债利差',linewidth=0.2)
ax2.plot(df['日期'], df['股债利差均线'], color='g', label='股债利差均线',alpha=0.2)
ax2.set_ylabel('股债利差', color='b')
ax2.tick_params(axis='y', labelcolor='b')
ax2.legend(loc='upper right')

plt.title('股债利差与沪深300指数趋势')
# 在起始位置和结束位置添加日期标注
start_annotation = df.iloc[0]['日期'].strftime('%Y-%m-%d')
end_annotation = df.iloc[-1]['日期'].strftime('%Y-%m-%d')

ax1.annotate(f'起始日期: {start_annotation}',
             xy=(df.iloc[0]['日期'], df.iloc[0]['沪深300指数']),
             xytext=(10, 30), textcoords='offset points',
             arrowprops=dict(arrowstyle='->', color='black'))

ax1.annotate(f'结束日期: {end_annotation}',
             xy=(df.iloc[-1]['日期'], df.iloc[-1]['沪深300指数']),
             xytext=(-110, -50), textcoords='offset points',
             arrowprops=dict(arrowstyle='->', color='black'))

# 保存图表为临时文件
chart_path2 = 'chart_temp2.png'
plt.savefig(chart_path2)
plt.close()


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
# 设置邮件参数
my_sender = '1074725704@qq.com'  # 发件人邮箱账号
my_pass = 'rqcvsqdbwdneicih'  # 发件人邮箱授权码
my_user = '1074725704@qq.com'  # 收件人邮箱账号，我这边发送给自己
subject = '日报'

body = f"""
<html>
    <body>
        <p>股债利差与沪深300指数趋势图：</p>
        <img src="cid:chart3.png"><br>
        <img src="cid:chart1.png"><br>
        <img src="cid:chart2.png"><br>
        <p>{text}</p>
        
    </body>
</html>
"""

# 创建带嵌入图片的邮件
message = MIMEMultipart()
message.attach(MIMEText(body, 'html'))
message['From'] = formataddr([my_sender, my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
message['To'] = formataddr(["drifterzy@163.com", "drifterzy@163.com"])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
message['Subject'] = subject
# 添加图表附件
with open(chart_path1, 'rb') as chart_file:
    image = MIMEImage(chart_file.read(), name='chart1.png')
    image.add_header('Content-ID', '<chart1.png>')
    message.attach(image)
# 添加图表附件
with open(chart_path2, 'rb') as chart_file:
    image = MIMEImage(chart_file.read(), name='chart2.png')
    image.add_header('Content-ID', '<chart2.png>')
    message.attach(image)
# 添加图表附件
with open(chart_path3, 'rb') as chart_file:
    image = MIMEImage(chart_file.read(), name='chart3.png')
    image.add_header('Content-ID', '<chart3.png>')
    message.attach(image)

# 发送邮件
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'your_email@gmail.com'
smtp_password = 'your_email_password'

server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
server.sendmail(my_sender, ["drifterzy@163.com", ], message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
server.quit()  # 关闭连接
print("邮件发送成功")
# 移除临时文件
import os
os.remove(chart_path1)
os.remove(chart_path2)