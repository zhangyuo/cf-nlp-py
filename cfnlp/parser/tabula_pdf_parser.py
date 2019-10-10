#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019-04-15 15:49
@Author  : zhangyu
@Contact : zhangycqupt@163.com
@File    : tabula_pdf_parser.py
@Software: PyCharm
@Site    : https://github.com/zhangyuo
"""
import tabula
from jpype import get_default_jvm_path

jvm_path = get_default_jvm_path()

df = tabula.read_pdf("/Users/zhangyu/Downloads/2015年陕西省财政预算执行情况和2016年财政预算（草案）.pdf", encoding='utf-8', pages='all')
print(df)
for indexs in df.index:
    print(df.loc[indexs].values[1].strip())

# tabula.convert_into(u"/Users/zhangyu/Downloads/2017年陕西省财政预算执行情况和2018年财政预算（草案）.pdf", '/Users/zhangyu/Downlodas/1.csv', all)
