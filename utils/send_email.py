import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import smtplib

def send_email_with_images(body,image_paths):
    # 设置邮件参数
    my_sender = '1074725704@qq.com'  # 发件人邮箱账号
    my_pass = 'rqcvsqdbwdneicih'  # 发件人邮箱授权码
    my_receiver = 'drifterzy@163.com'  # 收件人邮箱账号

    # 创建带嵌入图片的邮件
    message = MIMEMultipart()
    message.attach(MIMEText(body, 'html'))
    message['From'] = formataddr([my_sender, my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    message['To'] = formataddr([my_receiver, my_receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    message['Subject'] = '日报'

    # Attach images to the email
    for i, chart_path in enumerate(image_paths, start=1):
        with open(chart_path, 'rb') as chart_file:
            image = MIMEImage(chart_file.read(), name=f'chart{i}.png')
            image.add_header('Content-ID', f'<chart{i}.png>')
            message.attach(image)

    # 发送邮件
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
    server.sendmail(my_sender, [my_receiver, ], message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接
    print("邮件发送成功")
    # Remove temporary chart files
    for chart_path in image_paths:
        os.remove(chart_path)
