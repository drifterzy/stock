import pymysql

# 数据库连接信息
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}


def get_nearest_date(cursor, fund_code, target_date, is_start_date):
    """
    查找距离目标日期最近的日期。

    :param cursor: 数据库游标。
    :param fund_code: 基金代码。
    :param target_date: 目标日期。
    :param is_start_date: 是否为起始日期（True：查找不晚于目标日期的最近日期，False：查找不早于目标日期的最近日期）。
    :return: 最近日期或 None。
    """
    if is_start_date:
        # 查找不晚于目标日期的最近日期
        query = """
        SELECT net_value_date 
        FROM fund_net_value
        WHERE fund_code = %s AND net_value_date <= %s
        ORDER BY net_value_date DESC
        LIMIT 1
        """
    else:
        # 查找不早于目标日期的最近日期
        query = """
        SELECT net_value_date 
        FROM fund_net_value
        WHERE fund_code = %s AND net_value_date >= %s
        ORDER BY net_value_date ASC
        LIMIT 1
        """

    cursor.execute(query, (fund_code, target_date))
    result = cursor.fetchone()
    return result[0] if result else None


def calculate_return_rate(fund_code, start_date, end_date):
    """
    计算指定基金在给定日期范围内的收益率。

    :param fund_code: 基金代码。
    :param start_date: 起始日期（YYYY-MM-DD）。
    :param end_date: 结束日期（YYYY-MM-DD）。
    :return: 收益率（百分比）或错误信息。
    """
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 查找最接近的起始日期和结束日期
            actual_start_date = get_nearest_date(cursor, fund_code, start_date, is_start_date=True)
            actual_end_date = get_nearest_date(cursor, fund_code, end_date, is_start_date=False)

            if not actual_start_date or not actual_end_date:
                return f"无法找到起始日期或结束日期附近的交易记录"

            # 查询起始日期和结束日期的累计净值
            query = """
            SELECT net_value_date, cumulative_net_value 
            FROM fund_net_value
            WHERE fund_code = %s AND net_value_date IN (%s, %s)
            ORDER BY net_value_date
            """
            cursor.execute(query, (fund_code, actual_start_date, actual_end_date))
            results = cursor.fetchall()

        # 提取起始值和结束值
        values = {row[0]: row[1] for row in results}
        start_value = values.get(actual_start_date)
        end_value = values.get(actual_end_date)

        if start_value is None or end_value is None:
            return f"起始值或结束值缺失（日期范围：{actual_start_date} 至 {actual_end_date}）"

        # 计算收益率
        return_rate = ((end_value - start_value) / start_value) * 100
        return round(return_rate, 2), actual_start_date, actual_end_date

    except Exception as e:
        return f"发生错误：{e}"
    finally:
        connection.close()


# 示例调用
if __name__ == "__main__":
    fund_code = "007562"  # 基金代码
    start_date = "2024-01-01"  # 起始日期
    end_date = "2024-12-31"  # 结束日期
    # start_date = "2023-01-01"  # 起始日期
    # end_date = "2023-12-31"  # 结束日期
    # start_date = "2022-01-01"  # 起始日期
    # end_date = "2022-12-31"  # 结束日期
    # start_date = "2021-01-01"  # 起始日期
    # end_date = "2021-12-31"  # 结束日期
    result = calculate_return_rate(fund_code, start_date, end_date)
    if isinstance(result, tuple):
        return_rate, actual_start_date, actual_end_date = result
        print(f"基金 {fund_code} 在 {actual_start_date} 至 {actual_end_date} 的收益率为：{return_rate}%")
    else:
        print(result)
