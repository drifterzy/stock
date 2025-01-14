import sys
current_working_directory = "C:\project\stock"
sys.path.append(current_working_directory)
from image_module.kezhuanzhai import plot_kezhuanzhai
from utils import send_email
from image_module.etf300 import plot_etf300
from image_module.guzhailicha_partial import plot_guzhailicha_partial
from image_module.guzhailicha import plot_guzhailicha


if __name__ == "__main__":
    image_etf300 = plot_etf300()
    image_guzhailicha20211229 = plot_guzhailicha_partial()
    image_guzhailicha = plot_guzhailicha()
    image_kezhuanzhai = plot_kezhuanzhai()
    # 此处传入路径顺序则为显示顺序
    image_paths = [image_etf300,
                   image_guzhailicha20211229,
                   image_kezhuanzhai,
                   image_guzhailicha]
    text="测试"
    # 有几张图放几个png
    body = f"""
    <html>
        <body>
            <img src="cid:chart1.png"><br>
            <img src="cid:chart2.png"><br>
            <img src="cid:chart3.png"><br>
            <img src="cid:chart4.png"><br>
            <p>{text}</p>
        </body>
    </html>
    """

    send_email.send_email_with_images(body, image_paths)