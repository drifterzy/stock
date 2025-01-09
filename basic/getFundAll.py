import pymysql
import pandas as pd
from pathlib import Path

# 数据库配置
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "stock",
    "user": "root",
    "password": "123456",
}

# 文件路径配置
config = {
    "xlsx_file": "./data/allFundBasicData_cleaned.xlsx",
    "indicator_file": "./data/dbFundperformance.xlsx",
    "output_file": "./data/allFundResult.xlsx",
}

def get_earliest_dates_from_db(db_config):
    """
    从数据库获取每个基金代码的最早日期。

    参数:
    db_config: dict - 数据库连接配置。

    返回:
    DataFrame - 包含基金代码及其最早日期。
    """
    query = """
        SELECT fund_code, MIN(net_value_date) AS earliest_date
        FROM fund_net_value
        GROUP BY fund_code
    """
    try:
        connection = pymysql.connect(**db_config)
        earliest_dates_df = pd.read_sql(query, connection)
        connection.close()
    except Exception as e:
        raise RuntimeError(f"数据库查询失败: {e}")
    return earliest_dates_df

def merge_xlsx_with_indicators(xlsx_file, indicator_file, earliest_dates_df, output_file):
    # 加载 Excel 文件
    df_xlsx = pd.read_excel(xlsx_file)
    df_indicators = pd.read_excel(indicator_file)

    # 格式化基金代码为字符串
    df_xlsx['基金代码'] = df_xlsx['基金代码'].astype(str)
    df_indicators['基金代码'] = df_indicators['基金代码'].astype(str)  # 确保指标文件的基金代码是字符串
    earliest_dates_df['fund_code'] = earliest_dates_df['fund_code'].astype(str)

    # 转换日期格式
    df_xlsx['成立时间'] = pd.to_datetime(df_xlsx['成立时间'], errors='coerce')

    # 合并数据库中的最早日期到 xlsx 数据
    merged_xlsx = pd.merge(df_xlsx, earliest_dates_df, left_on='基金代码', right_on='fund_code', how='left')
    merged_xlsx['成立时间'] = merged_xlsx['earliest_date'].fillna(merged_xlsx['成立时间'])

    # 删除辅助列
    merged_xlsx.drop(columns=['earliest_date', 'fund_code'], inplace=True)

    # 合并指标文件
    final_merged_df = pd.merge(merged_xlsx, df_indicators, on='基金代码', how='left')

    # 保存结果到文件
    final_merged_df.to_excel(output_file, index=False)
    return final_merged_df


def main():
    try:
        # 从数据库获取最早日期
        print("正在从数据库获取最早日期...")
        earliest_dates_df = get_earliest_dates_from_db(db_config)

        # 合并数据并保存结果
        print("正在合并 xlsx 文件和指标文件...")
        final_df = merge_xlsx_with_indicators(
            config['xlsx_file'],
            config['indicator_file'],
            earliest_dates_df,
            config['output_file']
        )
        print(f"最终合并文件已保存到: {config['output_file']}")

    except Exception as e:
        print(f"执行过程中出现错误: {e}")

if __name__ == "__main__":
    main()
