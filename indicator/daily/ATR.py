import pymysql
import pandas as pd

# 数据库连接配置
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}


def calculate_atr(fund_code: str, period: int = 14):
    # 连接数据库
    connection = pymysql.connect(**db_config)

    try:
        # 查询指定基金代码的历史数据
        query = """
        SELECT fund_code, net_value_date, open_value, close_value, high_value, low_value
        FROM etf_net_value_qfq
        WHERE fund_code = %s
        ORDER BY net_value_date ASC;
        """
        df = pd.read_sql(query, connection, params=(fund_code,))
        df["net_value_date"] = pd.to_datetime(df["net_value_date"])  # 确保日期是日期格式
        # 计算真实波幅（True Range）
        df['previous_close'] = df['close_value'].shift(1)
        df['true_range'] = df[['high_value', 'low_value', 'previous_close']].apply(
            lambda row: max(row['high_value'] - row['low_value'],
                            abs(row['high_value'] - row['previous_close']),
                            abs(row['low_value'] - row['previous_close'])), axis=1
        )

        # 动态计算ATR（根据周期）
        atr_column_name = f'ATR{period}'  # 动态列名
        df[atr_column_name] = df['true_range'].rolling(window=period).mean()

        # 获取结果并返回
        result = df[['fund_code', 'net_value_date', 'open_value', 'close_value', 'high_value', 'low_value', 'true_range', atr_column_name]].dropna()

        return result

    finally:
        # 关闭数据库连接
        connection.close()


# 示例调用
# fund_code = '510300'
# period = 20  # 可以修改为其他周期，例如30, 60等
# atr_result = calculate_atr(fund_code, period)
# atr_result.to_excel(f'../data/{fund_code}_ATR_{period}.xlsx', index=False)
# print(atr_result)
