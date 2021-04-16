# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_image_task.py
   Description :  保存图片
   Author :       xlz

-------------------------------------------------
""" 
import os
from datetime import datetime
from os.path import abspath
import requests
import sys
import pandas as pd  
from hdbcli import dbapi



# 图片保存地址
PIC_PATH = "C:\product_image"
now = datetime.now()
today = now.strftime("%Y-%m-%d")
 
# 查询图片url
def select_picture_url():
    
    conn = dbapi.connect(
        address='10.150.16.99',
        port='30015',
        user='LINEZONEUSER',
        password='L1ne!2020'
    cursor = conn.cursor()
    sql_command = '''( select distinct KF_PIC 
    from linezoneuser.dim_sku
    where PRODUCT_YEAR >='2018'  
    and KF_PIC is not null ) t ''' 
    df= cursor.execute(sql_command)
    picture_url_df = lz_spark.spark.sql(sql).to_list()
    return picture_url_df.to_dict(orient='records')
 

def process_pool(pic_list):
    pool = Pool(processes=10)
    for link in pic_list:
        pool.apply_async(download_picture, (link, ))
    pool.close()
    pool.join()


# 下载图片
def download_picture(link):
    print(link)
    pic_path = PIC_PATH + link['skc_code'] + ".jpg"
    pic_link = link['kf_pic']
    pic = requests.get(pic_link, timeout=1)
    if pic.status_code == 200:
        with open(pic_path, 'wb') as fp:
            fp.write(pic.content)
            fp.close()
        print("===== 下载成功的skc ", link['skc_code'])
 

if __name__ == '__main__':
    print(datetime.now()), '=== 开发查询'
    picture_list = select_picture_url()
    pic_info = check_image(picture_list)
    print(datetime.now(), '===查询数据完成开始下载图片')
    if pic_info:
        print('===要下载 skc的个数', len(pic_info))
        process_pool(pic_info)
        print(datetime.now(), '===下载图片完成')
        update_table()
        print(datetime.now(), '===更新表完成')

