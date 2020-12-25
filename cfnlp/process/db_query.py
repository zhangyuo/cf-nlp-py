#!/usr/bin/env python
# coding:utf-8
"""
# @Time     : 2020-08-31 20:13
# @Author   : Zhangyu
# @Email    : zhangycqupt@163.com
# @File     : db_query.py
# @Software : PyCharm
# @Desc     :
"""
import datetime
import random
from time import sleep
import pandas as pd

from peewee import fn

from cfnlp.model.peewee_models import MysqlData, TestData


def count_query(job_ids, start_time, end_time):
    count_query = MysqlData.select(fn.COUNT(MysqlData.id)).where(
        (MysqlData.job_id.in_(job_ids)) &
        (MysqlData.create_time >= start_time) &
        (MysqlData.create_time <= end_time)
    )
    return count_query


def fetch_data_from_mysql_db_by_job_ids(job_ids, start_time, end_time, page_num, page_size):
    datas = MysqlData \
        .select(MysqlData.data, MysqlData.job_id) \
        .where((MysqlData.job_id.in_(job_ids)) &
               (MysqlData.create_time >= start_time) &
               (MysqlData.create_time <= end_time)) \
        .paginate(page_num, page_size)
    return datas


def insert_data_info(data):
    data["created_by"] = 'SYS'
    # data["created_at"] = datetime.datetime.now()
    data["updated_by"] = 'SYS'
    # data["updated_at"] = datetime.datetime.now()
    try:
        result = TestData.insert(data).execute()  # 需设置unique key(字段，重复插入时报错)
        return result
    except Exception as e:
        # 更新重复记录，等待其他线程执行一段时间，避免插入失败
        for _ in range(0, 3):
            sleep(random.random() / 3)
            if data.get("unique_key", ""):  # 重复字段
                result = TestData.update(data).where(TestData.unique_key == data["unique_key"]).execute()
                if result > 0:
                    return result


# 以下未非查询db数据库时非页准备数据
def test_prepare(path):
    data = pd.read_csv(path, encoding="gbk")
    return data.to_dict(orient="records")


def test_data_count(start_time, end_time, data):
    return len(data)


def query_data(start_time, end_time, page_num, page_size, data):
    start_index = page_num * page_size
    end_index = page_size + start_index

    return data[start_index:end_index]
