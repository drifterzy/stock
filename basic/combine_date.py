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

# 连接到 MySQL 数据库
connection = pymysql.connect(**db_config)

# 查询每个基金代码的最早日期
query = """
    SELECT fund_code, MIN(net_value_date) AS earliest_date
    FROM fund_net_value
    GROUP BY fund_code
"""

# 使用 Pandas 执行 SQL 查询并将结果存储到 DataFrame 中
earliest_dates_df = pd.read_sql(query, connection)

# 关闭数据库连接
connection.close()

# 读取 CSV 文件到 DataFrame
csv_file = './data/allFundHoldings.csv'  # 这里是你的 CSV 文件路径
df_csv = pd.read_csv(csv_file)
df_csv = df_csv[~df_csv['基金简称'].str.contains('后端')]
# 确保 '基金代码' 列和 'fund_code' 列都是字符串类型
df_csv['基金代码'] = df_csv['基金代码'].astype(str)
earliest_dates_df['fund_code'] = earliest_dates_df['fund_code'].astype(str)

# 将成立时间列转换为日期格式（如果需要）
df_csv['成立时间'] = pd.to_datetime(df_csv['成立时间'], errors='coerce')  # 如果原始数据有无效日期，设置为 NaT

# 合并 DataFrame：通过 fund_code 字段将最早日期合并到 CSV 数据
merged_df = pd.merge(df_csv, earliest_dates_df, left_on='基金代码', right_on='fund_code', how='left')

# 替换成立时间为最早日期
merged_df['成立时间'] = merged_df['earliest_date'].fillna(merged_df['成立时间'])  # 如果没有找到最早日期，保持原始成立时间

# 删除不再需要的列（例如：earliest_date, fund_code）
merged_df.drop(columns=['earliest_date', 'fund_code'], inplace=True)


# 将更新后的 DataFrame 保存回 CSV 文件
merged_df.to_csv('./data/allFundHoldings_combined.csv', index=False)

# 显示更新后的 DataFrame
print(merged_df)
