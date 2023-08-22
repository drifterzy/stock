from Ashare import *
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '1074725704@qq.com'  # 发件人邮箱账号
my_pass = 'rqcvsqdbwdneicih'  # 发件人邮箱授权码
my_user = '1074725704@qq.com'  # 收件人邮箱账号，我这边发送给自己
def mail(signal,user):
    try:
        msg = MIMEText(signal, 'plain', 'utf-8')
        msg['From'] = formataddr([my_sender, my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([user, user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "ETF轮动通知"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(my_sender, [user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print("邮件发送失败")

stock_dict = {'sh511010': '国债ETF:511010', 'sh510050': '上证50ETF:510050', 'sz159915': '创业板ETF:159915'}
product_list = []
today_list=[]
before_list=[]
rate_list=[]
rate_res = []
for stock in stock_dict.keys():
    product_list.append(stock_dict[stock])
    df = get_price(stock, frequency='1d', count=23)
    idx_before = df.index[0]
    idx_today = df.index[len(df)-1]

    before_price = df.loc[idx_before]['close']
    before_list.append(before_price)
    today_price = df.loc[idx_today]['close']
    today_list.append(today_price)
    rate = (today_price-before_price)/before_price
    rate_res.append(rate)
    rate_list.append("%.3f"%rate)
# 计算涨跌幅情况
maxIndex = rate_list.index(max(rate_list))
buySignal = list(stock_dict.items())[maxIndex][1]
if(max(rate_res)>0):
    signalStr = idx_today.strftime('%Y-%m-%d')+"：应该买入"+buySignal
else:
    signalStr = idx_today.strftime('%Y-%m-%d')+"：应该空仓"

before_list=[str(x) for x in before_list]
today_list=[str(x) for x in today_list]
rate_list=[str(x) for x in rate_list]

line1 = "产品名称 : "+"｜".join(product_list)+"\n"
line2 = idx_before.strftime('%Y-%m-%d')+"价格 ： "+"｜".join(before_list)+"\n"
line3 = idx_today.strftime('%Y-%m-%d')+"价格 ： "+"｜".join(today_list)+"\n"
line4 = "涨跌幅         ："+"｜".join(rate_list)+"\n"
res = line1+line2+line3+line4+signalStr

mail(res,"drifterzy@163.com")
mail(res,"223540840@qq.com")