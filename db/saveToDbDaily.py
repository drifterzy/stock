import pymysql
import pandas as pd
import akshare as ak
from datetime import datetime
# 数据库配置信息
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}


def update_fund_data():
    # 获取数据
    fund_open_fund_daily_em_df = ak.fund_open_fund_daily_em()

    # 找到最新日期的累计净值列
    latest_date_column = None
    for column in fund_open_fund_daily_em_df.columns:
        if "累计净值" in column:
            latest_date_column = column
            break

    if not latest_date_column:
        print("未找到累计净值列，无法处理数据。")
        return

    # 提取最新日期
    net_value_date = "-".join(latest_date_column.split("-")[:3])

    # 连接数据库
    connection = pymysql.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
    )

    try:
        with connection.cursor() as cursor:
            for index, row in fund_open_fund_daily_em_df.iterrows():
                fund_code = row["基金代码"]
                print("基金代码",fund_code)
                    # 将 NaN 或空字符串替换为 None
                cumulative_net_value = None if pd.isna(row[latest_date_column]) or row[latest_date_column] == "" else row[latest_date_column]

                # 检查基金代码是否存在
                select_query = """
                    SELECT COUNT(*) FROM fund_net_value WHERE fund_code = %s AND net_value_date = %s
                """
                cursor.execute(select_query, (fund_code, net_value_date))
                exists = cursor.fetchone()[0]

                if exists:
                    # 更新累计净值
                    update_query = """
                        UPDATE fund_net_value
                        SET cumulative_net_value = %s
                        WHERE fund_code = %s AND net_value_date = %s
                    """
                    cursor.execute(update_query, (cumulative_net_value, fund_code, net_value_date))
                else:
                    # 插入新记录
                    insert_query = """
                        INSERT INTO fund_net_value (fund_code, net_value_date, cumulative_net_value)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_query, (fund_code, net_value_date, cumulative_net_value))

                    # 提交事务
                    connection.commit()

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        return False

    finally:
        connection.close()
        return True


if __name__ == "__main__":
    try:
        # 调用函数
        result = update_fund_data()
        # 获取当前日期
        current_date = datetime.now().strftime("%Y-%m-%d")
        # 如果函数执行成功，写入文件
        if result:
            with open("C:\\Users\\leo\\Desktop\\update_status.txt", "a", encoding="utf-8") as file:
                file.write(f"{current_date} - 更新基金数据成功！\n")
            print("结果已写入文件：update_status.txt")
        else:
            with open("C:\\Users\\leo\\Desktop\\update_status.txt", "a", encoding="utf-8") as file:
                file.write(f"{current_date} - 更新基金数据失败。\n")
            print("更新失败的结果已写入文件：update_status.txt")
    except Exception as e:
        # 处理异常并写入错误信息
        current_date = datetime.now().strftime("%Y-%m-%d")
        with open("C:\\Users\\leo\\Desktop\\update_status.txt", "a", encoding="utf-8") as file:
            file.write(f"{current_date} - 更新基金数据时发生错误：{str(e)}\n")
        print("异常信息已写入文件：update_status.txt")
