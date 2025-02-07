import pymysql
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.series import SeriesLabel
from openpyxl.utils.dataframe import dataframe_to_rows


# 数据库连接信息
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}


# 文件1：获取基金数据和计算回撤
def fetch_fund_data_1(fund_code):
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
            df = pd.DataFrame(data, columns=["net_value_date", "cumulative_net_value"])
            df["cumulative_net_value"] = df["cumulative_net_value"].astype(float)
            return df
    finally:
        connection.close()


def calculate_drawdowns(df):
    max_value = 0
    drawdown_list = []
    historical_max_drawdown = 0

    for value in df["cumulative_net_value"]:
        if value > max_value:
            max_value = value
        drawdown = ((value - max_value) / max_value) * 100 if max_value != 0 else 0
        drawdown_list.append(drawdown)
        historical_max_drawdown = min(historical_max_drawdown, drawdown)

    df["drawdown"] = drawdown_list
    df["historical_max_drawdown"] = historical_max_drawdown
    df["drawdown"] = df["drawdown"].apply(lambda x: round(float(x), 2))
    df["historical_max_drawdown"] = round(float(historical_max_drawdown), 2)
    return df


# 文件2：获取基金数据和计算年化收益率
def fetch_fund_data_2(fund_codes, start_date):
    connection = pymysql.connect(**db_config)
    try:
        query = f"""
        SELECT fund_code, net_value_date, cumulative_net_value
        FROM fund_net_value
        WHERE fund_code IN ({','.join([f"'{code}'" for code in fund_codes])}) 
          AND net_value_date > '{start_date}'
        ORDER BY fund_code, net_value_date;
        """
        df = pd.read_sql(query, connection)
    finally:
        connection.close()
    return df


def calculate_annualized_yield(df):
    df["net_value_date"] = pd.to_datetime(df["net_value_date"])
    df = df.sort_values(["fund_code", "net_value_date"])
    df["7d_yield"] = df.groupby("fund_code")["cumulative_net_value"].diff(7) / df.groupby("fund_code")["cumulative_net_value"].shift(7)
    df["7d_annualized_yield"] = ((1 + df["7d_yield"]) ** (365 / 7)) - 1
    return df


# 将文件1和文件2的结果保存到一个 Excel 文件中
def save_results_to_excel(fund_codes_1, fund_codes_2, start_date, output_file="combined_report.xlsx"):
    wb = Workbook()

    # 文件1的结果保存到 Sheet1
    ws1 = wb.active
    ws1.title = "Drawdown Analysis"

    results = []
    for fund_code in fund_codes_1:
        fund_data = fetch_fund_data_1(fund_code)
        if not fund_data.empty:
            result = calculate_drawdowns(fund_data)
            latest_result = result.iloc[-1]
            results.append({
                "基金代码": fund_code,
                "日期": str(latest_result["net_value_date"]),
                "净值": float(latest_result["cumulative_net_value"]),
                "当前回撤": float(latest_result["drawdown"]),
                "最大回撤": float(latest_result["historical_max_drawdown"]),
            })

    if results:
        results_df = pd.DataFrame(results)
        rows = dataframe_to_rows(results_df, index=False, header=True)
        for row in rows:
            ws1.append(row)

    # 文件2的结果保存到 Sheet2
    ws2 = wb.create_sheet("Annualized Yield")

    fund_data = fetch_fund_data_2(fund_codes_2, start_date)
    if not fund_data.empty:
        fund_data = calculate_annualized_yield(fund_data)
        df_pivot = fund_data.pivot(index="net_value_date", columns="fund_code", values="7d_annualized_yield")

        rows = dataframe_to_rows(df_pivot, index=True, header=True)
        for row in rows:
            ws2.append(row)

        # 添加图表
        chart = LineChart()
        chart.title = "7-Day Annualized Yield (All Funds)"
        chart.style = 2
        chart.y_axis.title = "7-Day Annualized Yield"
        chart.x_axis.title = "Date"
        chart.x_axis.number_format = "yyyy-mm-dd"  # 设置横轴为日期格式
        chart.x_axis.majorTimeUnit = "days"  # 将横轴的单位设置为天
        chart.x_axis.tickLblPos = "low"  # X轴标签位置


        data = Reference(ws2, min_col=2, min_row=2, max_col=len(fund_codes_2) + 1, max_row=len(df_pivot) + 1)
        categories = Reference(ws2, min_col=1, min_row=2, max_row=len(df_pivot) + 1)

        for col_idx, fund_code in enumerate(fund_codes_2, start=2):
            data_ref = Reference(ws2, min_col=col_idx, min_row=2, max_row=len(df_pivot) + 1)
            chart.add_data(data_ref, titles_from_data=True)
            chart.series[-1].tx = SeriesLabel(v=f"{fund_code}")

        chart.set_categories(categories)

        # 设置图表大小
        chart.width = 30
        chart.height = 20

        ws2.add_chart(chart, "E5")

    # 保存文件

    wb.save(output_file)
    print(f"Combined results saved to {output_file}")


# 主函数
if __name__ == "__main__":
    # 已购产品止损
    fund_codes_1 = ["002920", "009219", "007582", "007319", "004839", "007562", "003657", "007229", "008383"]
    # 待购产品买入
    fund_codes_2 = ["007229"]
    start_date = "2024-01-01"
    output_file = "./gushouReport.xlsx"

    save_results_to_excel(fund_codes_1, fund_codes_2, start_date, output_file)
