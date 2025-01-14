import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from datetime import datetime

# 数据库相关代码和计算逻辑保持不变
# 此处假设 results 已经生成

def save_results_to_file(results, file_path):
    # 将结果保存为 Excel 表格
    df = pd.DataFrame(results)
    df.to_excel(file_path, index=False)
    print(f"Results saved to {file_path}")


def send_email_with_attachment(smtp_server, port, sender_email, sender_password, recipient_email, subject, body,
                               attachment_path):
    # 创建邮件消息
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, "plain"))

    # 添加附件
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={attachment_path.split('/')[-1]}",
    )
    msg.attach(part)
    current_date = datetime.now().strftime("%Y-%m-%d")
    try:
        # 连接 SMTP 服务器
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # 启用加密
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            with open("C:\\Users\\leo\\Desktop\\update_status.txt", "a", encoding="utf-8") as file:
                file.write(f"{current_date} - 发送邮件成功！\n")
            print("Email sent successfully.")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    # 保存文件（生成 .xlsx 文件）
    file_path = "../data/gushouReport.xlsx"

    # 邮件配置信息
    smtp_server = "smtp.qq.com"  # SMTP 服务器地址，例如 QQ 邮箱
    port = 587  # SMTP 端口
    sender_email = "1074725704@qq.com"  # 发件人邮箱
    sender_password = "rwkrjxtmadpphjei"  # 发件人邮箱密码或应用密码
    recipient_email = "drifterzy@163.com"  # 收件人邮箱
    subject = "Fund Report"
    body = "Please find the attached fund report."

    # 发送邮件
    send_email_with_attachment(
        smtp_server, port, sender_email, sender_password, recipient_email, subject, body, file_path
    )
