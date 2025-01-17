import pymysql
import pandas as pd

# 数据库配置
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}


def calculate_max_drawdown(fund_code, start_date, end_date):
    # 创建数据库连接
    connection = pymysql.connect(**db_config)

    try:
        # 查询指定时间段内的数据
        query = """
        SELECT net_value_date, cumulative_net_value 
        FROM fund_net_value 
        WHERE fund_code = %s AND net_value_date BETWEEN %s AND %s
        ORDER BY net_value_date;
        """
        df = pd.read_sql(query, connection, params=(fund_code, start_date, end_date))

        if df.empty:
            print("指定时间段内没有数据")
            return None

        # 计算最大回撤
        df['max_cumulative_value'] = df['cumulative_net_value'].cummax()  # 历史最大值
        df['drawdown'] = (df['cumulative_net_value'] - df['max_cumulative_value']) / df['max_cumulative_value']
        max_drawdown = df['drawdown'].min()  # 最大回撤值（最小的回撤）

        print(f"最大回撤 (Max Drawdown): {max_drawdown:.2%}")
        return max_drawdown, df  # 返回值和明细数据
    finally:
        connection.close()


# 示例调用
fund_code = "001316"
start_date = "2015-05-25"
end_date = "2024-05-22"
max_drawdown, details = calculate_max_drawdown(fund_code, start_date, end_date)

# 打印明细数据（可选）
if details is not None:
    print(details)
