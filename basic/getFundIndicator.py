import pandas as pd
import akshare as ak
import numpy as np
import time

# 指标计算函数
def calculate_annualized_return(df):
    start_value = df["累计净值"].iloc[0]
    end_value = df["累计净值"].iloc[-1]
    days = (pd.to_datetime(df["净值日期"].iloc[-1]) - pd.to_datetime(df["净值日期"].iloc[0])).days
    years = days / 365.0
    return (end_value / start_value) ** (1 / years) - 1


def calculate_max_drawdown(df):
    cummax = df["累计净值"].cummax()
    drawdown = (df["累计净值"] - cummax) / cummax
    return drawdown.min()


def calculate_annualized_volatility(df):
    # 处理缺失值或指定 fill_method
    df["每日收益率"] = df["累计净值"].pct_change(fill_method=None)  # 或填充缺失值后计算
    return df["每日收益率"].std() * np.sqrt(252)



def calculate_sharpe_ratio(df, risk_free_rate=0.02):
    annualized_return = calculate_annualized_return(df)
    volatility = calculate_annualized_volatility(df)
    return (annualized_return - risk_free_rate) / volatility


def calculate_calmar_ratio(df):
    annualized_return = calculate_annualized_return(df)
    max_drawdown = calculate_max_drawdown(df)
    return annualized_return / abs(max_drawdown)


def calculate_quarterly_win_rate(df):
    df["净值日期"] = pd.to_datetime(df["净值日期"])
    df["季度"] = df["净值日期"].dt.to_period("Q")
    quarterly_returns = df.groupby("季度")["累计净值"].last().pct_change()
    return (quarterly_returns > 0).mean()


def calculate_fund_metrics(df):
    return {
        "年化收益率": calculate_annualized_return(df),
        "最大回撤": calculate_max_drawdown(df),
        "年化波动率": calculate_annualized_volatility(df),
        "夏普率": calculate_sharpe_ratio(df),
        "卡玛率": calculate_calmar_ratio(df),
        "季度胜率": calculate_quarterly_win_rate(df),
    }


# 主函数：读取 CSV、遍历基金代码并计算指标
def process_fund_data(input_file, output_file):
    # 读取 CSV 文件
    funds_df = pd.read_csv(input_file)

    # 新增指标列
    metrics_columns = ["年化收益率", "最大回撤", "年化波动率", "夏普率", "卡玛率", "季度胜率"]
    for col in metrics_columns:
        funds_df[col] = None  # 初始化为空

    # 遍历基金代码
    for index, row in funds_df.iterrows():
        symbol = row["基金代码"]
        print(symbol)
        # 确保基金代码是字符串格式
        symbol = str(symbol).zfill(6)
        if pd.isna(symbol):  # 跳过空基金代码
            continue
        try:
            # 获取累计净值走势数据
            fund_data = ak.fund_open_fund_info_em(symbol=str(symbol), indicator="累计净值走势")
            if fund_data.empty:
                continue

            # 计算指标
            metrics = calculate_fund_metrics(fund_data)

            # 写入结果
            for col in metrics_columns:
                funds_df.loc[index, col] = metrics[col]

            time.sleep(0.5)
        except Exception as e:
            print(f"基金代码 {symbol} 的数据处理失败：{e}")
            # 在失败情况下显式写入空值
            for col in metrics_columns:
                funds_df.loc[index, col] = None


    # 保存结果到新的 CSV 文件
    funds_df.to_csv(output_file, index=False)
    print(f"处理完成，结果已保存到 {output_file}")


# 使用示例
input_csv = "./data/allFundHoldings.csv"  # 输入文件名
output_csv = "./data/allFundIndicators.csv"  # 输出文件名
process_fund_data(input_csv, output_csv)
