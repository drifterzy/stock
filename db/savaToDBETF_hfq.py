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
CREATE TABLE IF NOT EXISTS etf_net_value_hfq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fund_code VARCHAR(10) NOT NULL,
    net_value_date DATE NOT NULL,
    open_value DECIMAL(10, 4) NULL,
    close_value DECIMAL(10, 4) NULL,
    high_value DECIMAL(10, 4) NULL,
    low_value DECIMAL(10, 4) NULL,
    amount DECIMAL(10, 4) NULL,
    amount_value DECIMAL(10, 4) NULL,
    amplitude DECIMAL(10, 4) NULL,
    price_change DECIMAL(10, 4) NULL,
    price_change_rate DECIMAL(10, 4) NULL,
    turnover DECIMAL(10, 4) NULL,
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
    INSERT INTO etf_net_value (fund_code, net_value_date, open_value,close_value,high_value,low_value,amount,amount_value,amplitude,price_change,price_change_rate,turnover)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    open_value = VALUES(open_value),
    close_value = VALUES(close_value),
    high_value = VALUES(high_value),
    low_value = VALUES(low_value),
    amount = VALUES(amount),
    amount_value = VALUES(amount_value),
    amplitude = VALUES(amplitude),
    price_change = VALUES(price_change),
    price_change_rate = VALUES(price_change_rate),
    turnover = VALUES(turnover);
    """
    for _, row in data.iterrows():
        # 将 NaN 替换为 None
        open_value = None if np.isnan(row['开盘']) else row['开盘']
        close_value = None if np.isnan(row['收盘']) else row['收盘']
        high_value = None if np.isnan(row['最高']) else row['最高']
        low_value = None if np.isnan(row['最低']) else row['最低']
        amount = None if np.isnan(row['成交量']) else row['成交量']/10000
        amount_value = None if np.isnan(row['成交额']) else row['成交额']/100000000
        amplitude = None if np.isnan(row['振幅']) else row['振幅']
        price_change = None if np.isnan(row['涨跌幅']) else row['涨跌幅']
        price_change_rate = None if np.isnan(row['涨跌额']) else row['涨跌额']
        turnover = None if np.isnan(row['换手率']) else row['换手率']
        cur.execute(insert_query, (fund_code, row['日期'], open_value, close_value,high_value, low_value,
                                   amount, amount_value,amplitude, price_change,price_change_rate, turnover))
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
            # fund_open_fund_info_em_df = ak.fund_etf_fund_info_em(fund=fund_code, start_date="20000101", end_date="20500101")
            # fund_open_fund_info_em_df = ak.fund_etf_fund_info_em(fund=fund_code, start_date="20000101", end_date="20500101")
            fund_open_fund_info_em_df = ak.fund_etf_hist_em(symbol=fund_code, period="daily", start_date="20000101", end_date="20500101", adjust="hfq")
            insert_data(fund_code, fund_open_fund_info_em_df)
        except Exception as e:
            print(f"Error processing fund {fund_code}: {e}")

    print("All data processed and stored in the database.")
    end_time = time.time()  # 程序结束时间

    # 打印程序执行时间
    elapsed_time = end_time - start_time
    print(f"程序执行完毕，总耗时：{elapsed_time:.2f} 秒")  # 精确到小数点后2位
