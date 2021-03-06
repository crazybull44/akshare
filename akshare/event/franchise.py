# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/2/16 14:51
contact: jindaxiang@163.com
desc: 中国-商业特许经营信息管理
http://txjy.syggs.mofcom.gov.cn/
需要定期更新历史数据
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def _franchise_china_page_num():
    url = "http://txjy.syggs.mofcom.gov.cn/index.do"
    payload = {
        "method": "entps",
        "province": "",
        "city": "",
        "cpf.cpage": "1",
        "cpf.pagesize": "10",
    }
    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.text, "lxml")
    page_num = re.findall(re.compile(r"\d+"), soup.find(attrs={"class": "inner"}).find_all("a")[-1]["href"])[0]
    return int(page_num)


def franchise_china():
    """
    中国-商业特许经营信息管理
    http://txjy.syggs.mofcom.gov.cn/
    :return: 中国-商业特许经营的所有企业
    :rtype: pandas.DataFrame
    """
    url = "http://txjy.syggs.mofcom.gov.cn/index.do"
    # file_url 历史数据文件, 主要是为了防止重复访问的速度和资源浪费问题
    file_url = "https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/franchise/franchise_china.csv"
    outer_df = pd.read_csv(file_url, encoding="gbk", index_col=0)
    for page in range(1, int(5)):
        # print(page)
        payload = {
            "method": "entps",
            "province": "",
            "city": "",
            "cpf.cpage": str(page),
            "cpf.pagesize": "10",
        }
        r = requests.get(url, params=payload)
        temp_df = pd.read_html(r.text)[1]
        inner_df = temp_df.iloc[:, 0].str.split("  ", expand=True)
        inner_df.columns = ["特许人名称", "备案时间", "地址"]
        outer_df = outer_df.append(inner_df, ignore_index=True)
    outer_df.drop_duplicates(inplace=True)
    return outer_df


if __name__ == '__main__':
    franchise_china_df = franchise_china()
    print(franchise_china_df)
