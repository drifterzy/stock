import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '1074725704@qq.com'  # 发件人邮箱账号
my_pass = 'rqcvsqdbwdneicih'  # 发件人邮箱授权码
my_user = '1074725704@qq.com'  # 收件人邮箱账号，我这边发送给自己
def mail(signal,user, title=None):
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