import akshare as ak
import pymysql
import numpy as np
import time
# 数据库连接配置
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}

# 建表语句
create_table_query = """
CREATE TABLE IF NOT EXISTS etf_net_value (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fund_code VARCHAR(10) NOT NULL,
    net_value_date DATE NOT NULL,
    cumulative_net_value DECIMAL(10, 4) NULL,
    daily_growth_rate DECIMAL(10, 4) NULL,
    UNIQUE KEY unique_fund_date (fund_code, net_value_date)
);
"""

# 创建数据库连接和表
def setup_database():
    conn = pymysql.connect(**db_config)
    cur = conn.cursor()
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()

# 插入数据到数据库
def insert_data(fund_code, data):
    conn = pymysql.connect(**db_config)
    cur = conn.cursor()
    insert_query = """
    INSERT INTO etf_net_value (fund_code, net_value_date, cumulative_net_value,daily_growth_rate)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE cumulative_net_value = VALUES(cumulative_net_value),daily_growth_rate = VALUES(daily_growth_rate);
    """
    for _, row in data.iterrows():
        # 将 NaN 替换为 None
        cumulative_net_value = None if np.isnan(row['累计净值']) else row['累计净值']
        daily_growth_rate = None if np.isnan(row['日增长率']) else row['日增长率']
        cur.execute(insert_query, (fund_code, row['净值日期'], cumulative_net_value, daily_growth_rate))
    conn.commit()
    cur.close()
    conn.close()

# 主逻辑
if __name__ == "__main__":
    start_time = time.time()  # 程序开始时间
    # 初始化数据库
    setup_database()

    # 获取基金列表
    fund_name_em_df = ak.fund_etf_fund_daily_em()
    fund_list = fund_name_em_df[['基金代码', '基金简称', '类型']]

    # 遍历基金代码并获取累计净值走势
    for _, fund in fund_list.iterrows():
        fund_code = fund['基金代码']
        print(f"Processing fund: {fund_code}")
        try:
            fund_open_fund_info_em_df = ak.fund_etf_fund_info_em(fund=fund_code, start_date="20000101", end_date="20500101")
            insert_data(fund_code, fund_open_fund_info_em_df)
        except Exception as e:
            print(f"Error processing fund {fund_code}: {e}")

    print("All data processed and stored in the database.")
    end_time = time.time()  # 程序结束时间

    # 打印程序执行时间
    elapsed_time = end_time - start_time
    print(f"程序执行完毕，总耗时：{elapsed_time:.2f} 秒")  # 精确到小数点后2位
