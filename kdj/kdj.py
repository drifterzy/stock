#coding:utf-8
import baostock as bs
import pandas as pd
import matplotlib.pyplot as plt
def computeKDJ(code, startdate, enddate):
    # 获取股票日K线数据
    rs = bs.query_history_k_data_plus(code, "date,code,high,close,low,tradeStatus", start_date=startdate, end_date=enddate,
                                 frequency="d", adjustflag="2")
    # 打印结果集
    result_list = []
    while (rs.error_code == '0') & rs.next():
        result_list.append(rs.get_row_data())
    df_init = pd.DataFrame(result_list, columns=rs.fields)
    # print(df_init.head())
    # 剔除停盘数据
    df_status = df_init[df_init['tradeStatus'] == '1']
    low = df_status['low'].astype(float)
    del df_status['low']
    df_status.insert(0, 'low', low)
    high = df_status['high'].astype(float)
    del df_status['high']
    df_status.insert(0, 'high', high)
    close = df_status['close'].astype(float)
    del df_status['close']
    df_status.insert(0, 'close', close)
    # 计算KDJ指标,前8个数据为空，计算9天内的最高价，最低价
    low_list = df_status['low'].rolling(window=9).min()
    high_list = df_status['high'].rolling(window=9).max()
    rsv = (df_status['close'] - low_list) / (high_list - low_list) * 100
    df_data = pd.DataFrame()
    df_data['K'] = rsv.ewm(com=2).mean()
    df_data['D'] = df_data['K'].ewm(com=2).mean()
    df_data['J'] = 3 * df_data['K'] - 2 * df_data['D']
    df_data.index = df_status['date'].values
    df_data.index.name = 'date'
    # 删除空数据
    df_data = df_data.dropna()
    # 计算KDJ指标金叉、死叉情况
    df_data['KDJ_金叉死叉'] = ''
    kdj_position = df_data['K'] > df_data['D']
    df_data.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'
    df_data.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_金叉死叉'] = '死叉'
    # df_data.plot(title='KDJ')
    # plt.show()
    return(df_data)
if __name__ == '__main__':
    lg = bs.login()
    print(lg.error_msg)
    startdate = '2021-12-14'
    enddate = '2022-05-26'
    rs = bs.query_all_stock(day=enddate)
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    res_list = []
    for i in range(len(data_list)):
        code = data_list[i][0]
        code_name = data_list[i][2]
        if code.startswith( 'bj' ):
            continue
        df = computeKDJ(code, startdate, enddate)
        # if len(df.loc[(df.index == enddate) & (df["KDJ_金叉死叉"] == "金叉")]) == 1:
        if len(df.loc[(df.index == enddate) & (df["KDJ_金叉死叉"] == "金叉") & (df["D"] < 20)]) == 1:
            fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ"
            df_bs = bs.query_history_k_data(code, fields, start_date=enddate, end_date=enddate,
                                            frequency="d",adjustflag="2")
            stock_list = []
            while (df_bs.error_code == '0') & df_bs.next():
                # 获取一条记录，将记录合并在一起
                stock_list.append(df_bs.get_row_data())
            stock_list[0].insert(2, code_name)
            res_list.append(stock_list[0])
        # 保存到文件中
        # df.to_csv("./data/KDJ.csv", encoding='gbk')
    print (res_list)
    res_fields = ['date','code','code_name','open','high','low','close','preclose','volume','amount','adjustflag','turn','pctChg','peTTM','psTTM','pcfNcfTTM','pbMRQ']
    df_res = pd.DataFrame(res_list, columns=res_fields)
    df_res.to_csv("./data/0526.csv", encoding='gbk')
    bs.logout()