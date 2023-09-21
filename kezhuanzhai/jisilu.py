import akshare as ak
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import requests


# 通过集思录api获取可转债数据
def get_jsl_data():
    # 不打开浏览器
    options = webdriver.EdgeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    service = Service('C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe')
    web = webdriver.Edge(service=service, options=options)
    # 打开浏览器
    # web = webdriver.Edge()

    # 登陆
    web.get('https://www.jisilu.cn/account/login/')  # 打开登陆页
    web.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[2]/input').send_keys(
        '18813056645')  # 填入账号
    web.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[3]/input').send_keys(
        'a8867941')  # 填入密码
    web.find_element(By.XPATH,
                     '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[5]/div[1]/input').click()  # 勾选记住我
    web.find_element(By.XPATH,
                     '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[5]/div[2]/input').click()  # 勾选条款
    web.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[6]/a').click()  # 点击登陆
    time.sleep(0.2)

    # 登陆后要爬取https://www.jisilu.cn/data/cbnew/cb_list_new/的数据，修改下面代码
    web.get('https://www.jisilu.cn/data/cbnew/cb_list_new/')

    # 获取cookie
    cookie = web.get_cookies()

    # 关闭浏览器
    web.quit()
    headers_jsl = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110Safari/537.36',
        'Cookie': '; '.join([str(x['name']) + '=' + str(x['value']) for x in cookie])
    }
    url = 'https://www.jisilu.cn/data/cbnew/cb_list_new/'
    response = requests.get(url, headers=headers_jsl)
    data = response.json()
    df = pd.DataFrame(data["rows"])["cell"].apply(pd.Series)
    df = df.rename(
        columns={
            "bond_id": "代码",
            "bond_nm": "转债名称",
            "price": "现价",
            "increase_rt": "涨跌幅",
            "stock_id": "正股代码",
            "stock_nm": "正股名称",
            "sprice": "正股价",
            "sincrease_rt": "正股涨跌",
            "pb": "正股PB",
            "convert_price": "转股价",
            "convert_value": "转股价值",
            "premium_rt": "转股溢价率",
            "dblow": "双低",
            "rating_cd": "评级",
            "put_convert_price": "回售触发价",
            "force_redeem_price": "强赎触发价",
            "convert_amt_ratio": "转债流通市值占比",
            "maturity_dt": "到期时间",
            "year_left": "剩余年限",
            "curr_iss_amt": "剩余规模-亿",
            "volume": "成交额-万",
            "turnover_rt": "换手率",
            "ytm_rt": "到期税前收益",
            "real_force_redeem_price": "实时赎回价",
            "ref_yield_info": "纯债价值",
            "option_tip": "期权价值"
        },  # 对索引进行重命名
    )
    # df = df.drop(columns=['id'])        # 删除特定的列
    df = df[
        [
            "代码",
            "转债名称",
            "现价",
            "涨跌幅",
            "正股代码",
            "正股名称",
            "正股价",
            "正股涨跌",
            "正股PB",
            "转股价",
            "转股价值",
            "转股溢价率",
            "双低",
            "评级",
            "回售触发价",
            "强赎触发价",
            "转债流通市值占比",
            "到期时间",
            "剩余年限",
            "剩余规模-亿",
            "成交额-万",
            "换手率",
            "到期税前收益",
            "实时赎回价",
            "纯债价值",
            "期权价值"
        ]
    ]  # 保留的数据

    return df
df = get_jsl_data()
# 剔除未上市的新债
df = df[df['成交额-万'] != 0]
# 债性相关
df = df[df['正股PB'] >= 1]
df = df[df['到期税前收益'] >= 0]
df = df[df['剩余年限'] > 1]
df = df[df['剩余规模-亿'] < 5]
df = df[df['现价'] < 125]
df = df[~df['评级'].str.contains('B')]
df = df[~df['评级'].str.contains('^A\-', regex=True)]
df.to_csv('可转债.csv', index=False)
print("ok")