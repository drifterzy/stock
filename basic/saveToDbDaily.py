import pymysql
import pandas as pd
import akshare as ak

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
                if fund_code == '160213':
                    print("jgeg")
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

    finally:
        connection.close()


if __name__ == "__main__":
    update_fund_data()
