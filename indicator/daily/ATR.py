import pymysql
import pandas as pd

# MySQL连接配置
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}
def calculate_atr(fund_code):
    # 连接MySQL数据库
    connection = pymysql.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

    try:
        # 获取基金的历史净值数据
        query = f"""
        SELECT fund_code, net_value_date, cumulative_net_value, daily_growth_rate
        FROM etf_net_value
        WHERE fund_code = %s
        ORDER BY net_value_date
        """

        df = pd.read_sql(query, connection, params=(fund_code,))

        # 计算日波动幅度
        df['daily_range'] = df['cumulative_net_value'].pct_change() * 100  # 转化为百分比波动幅度

        # 计算ATR，取过去14天的平均值（可以根据需求调整周期）
        df['atr'] = df['daily_range'].rolling(window=14).mean()

        # 只保留需要的字段
        result = df[['fund_code', 'net_value_date', 'cumulative_net_value', 'atr']]

        return result.dropna()  # 去除无效数据（没有足够数据计算ATR）

    finally:
        connection.close()


# 示例调用
fund_code = '510300'
atr_data = calculate_atr(fund_code)
print(atr_data)
