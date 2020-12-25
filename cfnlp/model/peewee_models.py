#!/usr/bin/env python
# coding:utf-8
"""
# @Time     : 2020-08-12 19:59
# @Author   : Zhangyu
# @Email    : zhangycqupt@163.com
# @File     : peewee_models.py
# @Software : PyCharm
# @Desc     :
"""

from peewee import Model, AutoField, CharField, IntegerField, DateTimeField
from playhouse.pool import PooledMySQLDatabase

db_config = {
    "user": "xx",
    "password": "XX",
    "host": "XX.XX.xx.xx",
    "port": "xx"
}

mysql_db = PooledMySQLDatabase("spidercontrol", max_connections=200, **db_config)  # datbase: spidercontrol
insert_db = PooledMySQLDatabase("fapai", max_connections=200, **db_config)  # datbase: fapai


class MysqlData(Model):
    id = AutoField(primary_key=True)
    data = CharField()
    job_id = IntegerField()
    create_time = DateTimeField()

    class Meta:
        database = mysql_db
        table_name = 'fetch_table'


class TestData(Model):
    id = AutoField(primary_key=True)
    created_by = CharField()
    created_at = DateTimeField()
    updated_by = CharField()
    updated_at = DateTimeField()
    name = CharField()
    unique_key = CharField()

    class Meta:
        database = insert_db
        table_name = 'insert_table'
