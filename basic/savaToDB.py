import akshare as ak
import pymysql
import numpy as np

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
CREATE TABLE IF NOT EXISTS fund_net_value (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fund_code VARCHAR(10) NOT NULL,
    net_value_date DATE NOT NULL,
    cumulative_net_value DECIMAL(10, 4) NULL,
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
    INSERT INTO fund_net_value (fund_code, net_value_date, cumulative_net_value)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE cumulative_net_value = VALUES(cumulative_net_value);
    """
    for _, row in data.iterrows():
        # 将 NaN 替换为 None
        cumulative_net_value = None if np.isnan(row['累计净值']) else row['累计净值']
        cur.execute(insert_query, (fund_code, row['净值日期'], cumulative_net_value))
    conn.commit()
    cur.close()
    conn.close()

# 主逻辑
if __name__ == "__main__":
    # 初始化数据库
    setup_database()

    # 获取基金列表
    fund_name_em_df = ak.fund_name_em()
    fund_list = fund_name_em_df[['基金代码', '基金简称', '基金类型']]

    # 遍历基金代码并获取累计净值走势
    for _, fund in fund_list.iterrows():
        fund_code = fund['基金代码']
        print(f"Processing fund: {fund_code}")
        try:
            fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol=fund_code, indicator="累计净值走势")
            insert_data(fund_code, fund_open_fund_info_em_df)
        except Exception as e:
            print(f"Error processing fund {fund_code}: {e}")

    print("All data processed and stored in the database.")
