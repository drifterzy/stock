import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.series import SeriesLabel


def generate_line_chart_from_dataframe(dataframe, output_path, title="Capital Curve Comparison"):
    """
    从 DataFrame 的两列生成折线图的 Excel 文件。

    :param dataframe: 包含 `date` 和多列 `capital_curve` 的 DataFrame。
    :param output_path: 输出文件路径。
    :param title: 图表标题。
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame.")

    # 检查数据是否包含必要列
    if "date" not in dataframe.columns:
        raise ValueError("The DataFrame must contain a 'date' column.")

    # 检查是否有至少一个资本曲线列
    capital_columns = [col for col in dataframe.columns if col != "date"]
    if not capital_columns:
        raise ValueError("The DataFrame must contain at least one capital curve column.")

    # 创建 Excel 工作簿
    wb = Workbook()
    wb.remove(wb.active)

    # 创建新表
    sheet = wb.create_sheet(title=title[:30])

    # 写入日期和资本曲线数据
    sheet.append(["Date"] + capital_columns)
    for i, row in dataframe.iterrows():
        sheet.append([row["date"]] + [row[col] for col in capital_columns])

    # 创建折线图
    chart = LineChart()
    chart.title = title

    # 添加数据到图表
    for col_idx, label in enumerate(capital_columns, start=2):
        data_ref = Reference(sheet, min_col=col_idx, min_row=2, max_row=len(dataframe) + 1)
        chart.add_data(data_ref, titles_from_data=True)
        chart.series[-1].tx = SeriesLabel(v=label)

    # 添加 X 轴分类
    categories_ref = Reference(sheet, min_col=1, min_row=2, max_row=len(dataframe) + 1)
    chart.set_categories(categories_ref)

    # 自动设置图表大小
    chart.width = 30
    chart.height = 20

    # 添加图表到工作表
    sheet.add_chart(chart, "K2")

    # 保存 Excel 文件
    wb.save(output_path)
    print(f"Line chart created and saved to {output_path}!")


# 示例调用
if __name__ == "__main__":
    # 示例 DataFrame
    data = {
        "date": pd.date_range(start="2023-01-01", periods=10),
        "Fund A": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145]
    }
    df = pd.DataFrame(data)

    # 输出文件路径
    output_file = "output/capital_curve_chart.xlsx"

    # 调用生成图表函数
    generate_line_chart_from_dataframe(df, output_file)
