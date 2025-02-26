import pymysql
import pandas as pd
from datetime import datetime

# MySQL连接配置
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}


def calculate_ma(fund_code, ma_days=40):
    """
    计算指定基金的移动平均。

    :param fund_code: 基金代码
    :param ma_days: 移动平均的天数（如40日或100日）
    :return: 包含移动平均和累计净值的DataFrame
    """
    # 连接MySQL数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    try:
        # 查询特定基金的净值数据，按日期排序
        query = """
        SELECT fund_code, net_value_date, cumulative_net_value
        FROM etf_net_value
        WHERE fund_code = %s
        ORDER BY net_value_date;
        """
        cursor.execute(query, (fund_code,))
        data = cursor.fetchall()

        # 如果没有数据，直接返回空的DataFrame
        if not data:
            return pd.DataFrame()

        # 将查询结果转换为DataFrame
        df = pd.DataFrame(data, columns=["fund_code", "net_value_date", "cumulative_net_value"])
        df["net_value_date"] = pd.to_datetime(df["net_value_date"])  # 确保日期是日期格式

        # 计算指定天数的移动平均
        ma_column = f"ma{ma_days}"
        df[ma_column] = df["cumulative_net_value"].rolling(window=ma_days, min_periods=1).mean()

        # 返回结果，包括基金代码、日期、当日净值以及指定天数的MA列
        return df[["fund_code", "net_value_date", "cumulative_net_value", ma_column]]

    except Exception as e:
        print("查询或计算出现错误:", e)
        return pd.DataFrame()
    finally:
        cursor.close()
        conn.close()



"""
获取指定基金的40日和100日均线，并合并成一个DataFrame。

:param fund_code: 基金代码
:return: 包含40日和100日均线的DataFrame
"""
# 获取40日均线
result_40 = calculate_ma('510300', ma_days=40)

# 获取100日均线
result_100 = calculate_ma('510300', ma_days=100)

# 合并40日和100日均线的结果
combined_result = pd.merge(result_40, result_100, on=["fund_code", "net_value_date", "cumulative_net_value"],
                           how="outer")
combined_result.to_excel('../data/510300.xlsx', index=False)
# 打印合并后的结果
print(combined_result)


