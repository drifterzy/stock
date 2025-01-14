import pymysql
import pandas as pd

# 数据库连接信息
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}


# 获取基金数据
def fetch_fund_data(fund_code):
    query = f"""
    SELECT net_value_date, cumulative_net_value
    FROM fund_net_value
    WHERE fund_code = %s
    ORDER BY net_value_date ASC
    """
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (fund_code,))
            data = cursor.fetchall()
            # 转为 Pandas DataFrame，并将 Decimal 转换为 float
            df = pd.DataFrame(data, columns=["net_value_date", "cumulative_net_value"])
            df["cumulative_net_value"] = df["cumulative_net_value"].astype(float)
            return df
    finally:
        connection.close()


# 计算回撤和历史最大回撤
def calculate_drawdowns(df):
    max_value = 0
    drawdown_list = []
    historical_max_drawdown = 0

    for value in df["cumulative_net_value"]:
        if value > max_value:
            max_value = value  # 更新最高点
        drawdown = ((value - max_value) / max_value) * 100 if max_value != 0 else 0
        drawdown_list.append(drawdown)

        # 更新历史最大回撤
        historical_max_drawdown = min(historical_max_drawdown, drawdown)

    df["drawdown"] = drawdown_list
    df["historical_max_drawdown"] = historical_max_drawdown

    # 保留两位小数并确保类型为 float
    df["drawdown"] = df["drawdown"].apply(lambda x: round(float(x), 2))
    df["historical_max_drawdown"] = round(float(historical_max_drawdown), 2)

    return df


# 获取最新一天的数据
def get_latest_data(df):
    latest_data = df.iloc[-1]  # 获取最新一天的数据
    return latest_data


# 主函数
if __name__ == "__main__":
    fund_codes = ["002920", "009219", "007582", "007319", "004839"]  # 示例基金代码数组
    results = []

    for fund_code in fund_codes:
        fund_data = fetch_fund_data(fund_code)
        if not fund_data.empty:
            result = calculate_drawdowns(fund_data)
            latest_result = get_latest_data(result)
            results.append({
                "基金代码": fund_code,
                "日期": str(latest_result["net_value_date"]),
                "净值": float(latest_result["cumulative_net_value"]),
                "当前回撤": float(latest_result["drawdown"]),
                "最大回撤": float(latest_result["historical_max_drawdown"])
            })
        else:
            print(f"No data found for fund code: {fund_code}")

    # 将结果保存到 Excel 文件
    if results:
        results_df = pd.DataFrame(results)
        output_file = "../data/gushouReport.xlsx"
        results_df.to_excel(output_file, index=False, sheet_name="Fund Analysis")
        print(f"Results have been saved to {output_file}")

    # 打印结果，确保只显示数值
    for res in results:
        print(res)
