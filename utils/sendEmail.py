import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr
from datetime import datetime

def send_email_with_attachments(smtp_server, port, sender_email, sender_password, recipient_email, subject, body,
                                 attachment_title_mapping):
    # 创建邮件消息
    msg = MIMEMultipart()
    msg["From"] = formataddr((str(Header("邮件发送人", "utf-8")), sender_email))  # 设置发件人信息（支持中文）
    msg["To"] = recipient_email
    msg["Subject"] = Header(subject, "utf-8")  # 邮件主题支持中文

    # 添加邮件正文
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # 添加附件并设置自定义标题（支持中文文件名）
    for attachment_path, custom_title in attachment_title_mapping.items():
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)

            # 使用 Header 对中文标题进行 MIME 编码
            encoded_title = Header(custom_title, "utf-8").encode()
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{encoded_title}"',
            )
            msg.attach(part)
        except Exception as e:
            print(f"Failed to attach {attachment_path}: {e}")

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
    # 路径与自定义标题的映射
    attachment_title_mapping = {
        "C:\\project\\stock\\gushou\\report\\gushouReport.xlsx": "固收日报.xlsx",
        "C:\\project\\stock\\basic\\report\\basicReport.xlsx": "基础日报.xlsx",
    }

    # 邮件配置信息
    smtp_server = "smtp.qq.com"  # SMTP 服务器地址，例如 QQ 邮箱
    port = 587  # SMTP 端口
    sender_email = "1074725704@qq.com"  # 发件人邮箱
    sender_password = "rwkrjxtmadpphjei"  # 发件人邮箱密码或应用密码
    recipient_email = "drifterzy@163.com"  # 收件人邮箱
    subject = "Fund Report"
    body = "Please find the attached fund reports."

    # 发送邮件
    send_email_with_attachments(
        smtp_server, port, sender_email, sender_password, recipient_email, subject, body, attachment_title_mapping
    )
