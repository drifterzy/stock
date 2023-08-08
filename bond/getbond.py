import akshare as ak
import os
# 获取当前脚本文件所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构建输出文件的完整路径
output_dir = os.path.join(script_dir, '..', 'data')  # 回退到上级目录，然后进入"data"目录
output_file = '人事调整.xlsx'  # 输出文件名
output_path = os.path.join(output_dir, output_file)

# 基金基本信息
# fund_name_em_df = ak.fund_name_em()

# 基金实时数据
# fund_open_fund_daily_em_df = ak.fund_open_fund_daily_em()

# 基金历史数据 ：fund代码从基金实时数据出
# 基金历史数据-单位净值走势
# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund="004685", indicator="单位净值走势")
# 基金历史数据-累计净值走势
# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund="004685", indicator="累计净值走势")
# 基金历史数据-累计收益率走势
# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund="004685", indicator="累计收益率走势")
# 基金历史数据-同类排名走势
# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund="004685", indicator="同类排名走势")
# 基金历史数据-同类排名百分比
# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund="004685", indicator="同类排名百分比")
# 基金历史数据-分红送配详情
# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund="004685", indicator="分红送配详情")
# 基金历史数据-拆分详情
# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund="004685", indicator="拆分详情")

# 股票持仓
# fund_portfolio_hold_em_df = ak.fund_portfolio_hold_em(symbol="004685", date="2023")
# 债券持仓
# fund_portfolio_bond_hold_em_df = ak.fund_portfolio_bond_hold_em(symbol="004685", date="2023")

# 基金规模
# fund_scale_open_sina_df = ak.fund_scale_open_sina(symbol='股票型基金')

# 基金经理变更
fund_announcement_personnel_em_df = ak.fund_announcement_personnel_em(symbol="000001")
# 基金评级、基金行业配比
try:
    fund_announcement_personnel_em_df.to_excel(output_path, index=False)
    print(f"DataFrame已保存到 {output_path}")
except AttributeError as e:
    print("发生错误：", e)

