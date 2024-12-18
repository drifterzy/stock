import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_annualized_return(df):
    start_value = df["累计净值"].iloc[0]
    end_value = df["累计净值"].iloc[-1]
    days = (pd.to_datetime(df["净值日期"].iloc[-1]) - pd.to_datetime(df["净值日期"].iloc[0])).days
    years = days / 365.0
    annualized_return = (end_value / start_value) ** (1 / years) - 1
    return annualized_return

def calculate_max_drawdown(df):
    cummax = df["累计净值"].cummax()
    drawdown = (df["累计净值"] - cummax) / cummax
    max_drawdown = drawdown.min()
    return max_drawdown

def calculate_annualized_volatility(df):
    df["每日收益率"] = df["累计净值"].pct_change()
    volatility = df["每日收益率"].std() * np.sqrt(252)
    return volatility

def calculate_sharpe_ratio(df, risk_free_rate=0.02):
    annualized_return = calculate_annualized_return(df)
    volatility = calculate_annualized_volatility(df)
    sharpe_ratio = (annualized_return - risk_free_rate) / volatility
    return sharpe_ratio

def calculate_calmar_ratio(df):
    annualized_return = calculate_annualized_return(df)
    max_drawdown = calculate_max_drawdown(df)
    calmar_ratio = annualized_return / abs(max_drawdown)
    return calmar_ratio

def calculate_quarterly_win_rate(df):
    df["净值日期"] = pd.to_datetime(df["净值日期"])
    df["季度"] = df["净值日期"].dt.to_period("Q")
    quarterly_returns = df.groupby("季度")["累计净值"].last().pct_change()
    win_rate = (quarterly_returns > 0).mean()
    return win_rate

def calculate_fund_metrics(df):
    annualized_return = calculate_annualized_return(df)
    max_drawdown = calculate_max_drawdown(df)
    annualized_volatility = calculate_annualized_volatility(df)
    sharpe_ratio = calculate_sharpe_ratio(df)
    calmar_ratio = calculate_calmar_ratio(df)
    quarterly_win_rate = calculate_quarterly_win_rate(df)

    metrics = {
        "年化收益率": annualized_return,
        "最大回撤": max_drawdown,
        "年化波动率": annualized_volatility,
        "夏普率": sharpe_ratio,
        "卡玛率": calmar_ratio,
        "季度胜率": quarterly_win_rate
    }
    return metrics


fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol="004832", indicator="累计净值走势")
metrics = calculate_fund_metrics(fund_open_fund_info_em_df)
for key, value in metrics.items():
    print(f"{key}: {value:.4f}")


