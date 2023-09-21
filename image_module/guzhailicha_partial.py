import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd


def plot_guzhailicha_partial():
    # 设置编码格式，防止中文乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 获取股债利差值
    df = ak.stock_ebs_lg()
    # 获取21-12-29之后的数据
    start_date = pd.to_datetime('2021-12-29')
    df = df[df['日期'] >= start_date]
    # 绘制图表
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 绘制沪深300指数
    ax1.plot(df['日期'], df['沪深300指数'], color='r', label='沪深300指数')
    ax1.set_xlabel('日期')
    ax1.set_ylabel('沪深300指数', color='r')
    ax1.tick_params(axis='y', labelcolor='r')
    ax1.legend(loc='upper left')

    # 绘制股债利差和股债利差均线
    ax2 = ax1.twinx()
    ax2.plot(df['日期'], df['股债利差'], color='b', label='股债利差',linewidth=0.2)
    ax2.plot(df['日期'], df['股债利差均线'], color='g', label='股债利差均线',alpha=0.2)
    ax2.set_ylabel('股债利差', color='b')
    ax2.tick_params(axis='y', labelcolor='b')
    ax2.legend(loc='upper right')

    plt.title('股债利差与沪深300指数趋势-20211229')
    # 在起始位置和结束位置添加日期标注
    start_annotation = df.iloc[0]['日期'].strftime('%Y-%m-%d')
    end_annotation = df.iloc[-1]['日期'].strftime('%Y-%m-%d')

    ax1.annotate(f'起始日期: {start_annotation}',
                 xy=(df.iloc[0]['日期'], df.iloc[0]['沪深300指数']),
                 xytext=(10, 30), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='black'))

    ax1.annotate(f'结束日期: {end_annotation}',
                 xy=(df.iloc[-1]['日期'], df.iloc[-1]['沪深300指数']),
                 xytext=(-110, -50), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='black'))

    # 保存图表为临时文件
    chart_tmp = 'chart_guzhailicha_20211229.png'
    plt.savefig(chart_tmp)
    plt.close()
    return chart_tmp
