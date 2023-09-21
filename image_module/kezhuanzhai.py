import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd

def plot_kezhuanzhai():
    # 设置编码格式，防止中文乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df = ak.bond_cb_index_jsl()
    print(df)
    # 将 'price_dt' 列转换为日期时间类型
    df['price_dt'] = pd.to_datetime(df['price_dt'])
    start_date = pd.to_datetime('2023-01-01')
    df = df[df['price_dt'] >= start_date]
    df.set_index('price_dt', inplace=True)

    # 计算 price1 和 price2 的归一化值
    price1_normalized = df['price'] / df['price'].iloc[0]
    price2_normalized = df['idx_price'] / df['idx_price'].iloc[0]

    # 使用 matplotlib 绘制图表
    plt.figure(figsize=(10, 6))  # 设置图表的大小
    plt.plot(df.index, price1_normalized, label='转债等权', linewidth=0.2)  # 绘制归一化后的 price1 数据
    plt.plot(df.index, price2_normalized, label='沪深300', linewidth=0.2)  # 绘制归一化后的 price2 数据

    # 添加标签和图例
    plt.xlabel('Time')
    plt.ylabel('Normalized Price')
    plt.title('转债等权vs沪深300')
    plt.legend()

    # 显示图表
    plt.grid(True)
    plt.show()
    # df['price'] = df['price'] / df.loc[0, 'price']
    # df['idx_price'] = df['idx_price'] / df.loc[0, 'idx_price']
    # # 绘制图表
    # fig, ax1 = plt.subplots(figsize=(10, 6))
    #
    # # 绘制沪深300指数
    # ax1.plot(df['price_dt'], df['price'], color='r', label='转债等权指数')
    # ax1.set_xlabel('日期')
    # ax1.set_ylabel('转债等权指数', color='r')
    # ax1.tick_params(axis='y', labelcolor='r')
    # ax1.legend(loc='upper left')
    #
    # # 绘制股债利差和股债利差均线
    # ax2 = ax1.twinx()
    # ax2.plot(df['price_dt'], df['idx_price'], color='b', label='沪深300指数',linewidth=0.2)
    # ax2.set_ylabel('沪深300指数', color='b')
    # ax2.tick_params(axis='y', labelcolor='b')
    # ax2.legend(loc='upper right')
    #
    # plt.title('转债等权指数与沪深300指数趋势')
    # # 在起始位置和结束位置添加日期标注
    # start_annotation = df.iloc[0]['price_dt'].strftime('%Y-%m-%d')
    # end_annotation = df.iloc[-1]['price_dt'].strftime('%Y-%m-%d')
    #
    # ax1.annotate(f'起始日期: {start_annotation}',
    #              xy=(df.iloc[0]['price_dt'], df.iloc[0]['price']),
    #              xytext=(10, 30), textcoords='offset points',
    #              arrowprops=dict(arrowstyle='->', color='black'))
    #
    # ax1.annotate(f'结束日期: {end_annotation}',
    #              xy=(df.iloc[-1]['price_dt'], df.iloc[-1]['idx_price']),
    #              xytext=(-110, -50), textcoords='offset points',
    #              arrowprops=dict(arrowstyle='->', color='black'))
    #
    # # 保存图表为临时文件
    # chart_tmp = 'chart_kezhuanzhai.png'
    # plt.savefig(chart_tmp)
    # plt.close()
    # return chart_tmp

plot_kezhuanzhai()