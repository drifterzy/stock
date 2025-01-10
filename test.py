import pymysql
import pandas as pd
import matplotlib.pyplot as plt

# 数据库连接配置
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}

# 设置要计算的基金代码
fund_code_to_plot = "007229"

# 创建数据库连接
connection = pymysql.connect(**db_config)

try:
    # 仅查询指定基金代码的数据
    query = f"""
    SELECT fund_code, net_value_date, cumulative_net_value
    FROM fund_net_value
    WHERE fund_code = '{fund_code_to_plot}' and net_value_date>'2021-01-01'
    ORDER BY net_value_date;
    """
    df = pd.read_sql(query, connection)
finally:
    # 确保关闭数据库连接
    connection.close()

# 确保日期列为datetime类型
df['net_value_date'] = pd.to_datetime(df['net_value_date'])

# 按日期排序（确保顺序正确）
df = df.sort_values('net_value_date')

# 计算7日年化收益率
df['7d_yield'] = df['cumulative_net_value'].diff(7) / df['cumulative_net_value'].shift(7)  # 近7日变化百分比
df['7d_annualized_yield'] = ((1 + df['7d_yield']) ** (365 / 7)) - 1  # 年化收益率

# 绘制近7日年化收益率曲线
plt.figure(figsize=(10, 6))
plt.plot(df['net_value_date'], df['7d_annualized_yield'], label=f"Fund {fund_code_to_plot}")
plt.title(f"7-Day Annualized Yield for Fund {fund_code_to_plot}")
plt.xlabel("Date")
plt.ylabel("7-Day Annualized Yield")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
