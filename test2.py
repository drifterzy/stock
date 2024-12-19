import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def calculate_fund_annual_return(*fund_codes):
    """
    计算多个基金近一年的收益率
    :param fund_codes: 不定长参数，传入多个基金代码
    :return: DataFrame，包含基金代码和收益率
    """
    results = []

    # 获取当前日期和一年前的日期
    today = datetime.today()
    one_year_ago = today - timedelta(days=365)

    for code in fund_codes:
        code = str(code).zfill(6)
        if code == '002920':
            print("here")
        # 获取基金累计净值数据
        fund_data = ak.fund_open_fund_info_em(symbol=str(code), indicator="累计净值走势")
        fund_data["净值日期"] = pd.to_datetime(fund_data["净值日期"])
        fund_data = fund_data.sort_values("净值日期")

        # 筛选最近一年的数据
        recent_data = fund_data[fund_data["净值日期"] >= one_year_ago]

        if recent_data.empty:
            print(f"基金代码 {code} 没有足够的数据计算收益率")
            continue

        # 获取最新净值和一年前的净值
        latest_value = recent_data.iloc[-1]["累计净值"]
        initial_value = recent_data.iloc[0]["累计净值"]

        # 计算收益率
        annual_return = (latest_value - initial_value) / initial_value
        results.append({"基金代码": code, "近一年收益率": annual_return})

    # 将结果转换为 DataFrame
    results_df = pd.DataFrame(results)
    return results_df

# 调用函数计算20个基金的近一年收益率
fund_returns = calculate_fund_annual_return(
    6966, 6965, 7456, 6824, 9617, 6829, 7582, 5838, 6434, 2920,
    7014, 9721, 6516, 7015, 6076, 6825, 9087, 10810, 8820, 9219
)

# 打印结果
print(fund_returns)

# 保存到 CSV 文件
fund_returns.to_csv("fund_annual_returns.csv", index=False, encoding="utf-8-sig")
