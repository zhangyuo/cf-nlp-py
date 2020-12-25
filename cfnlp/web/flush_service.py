#!/usr/bin/env python
# coding:utf-8
"""
# @Time     : 2020-08-12 15:51
# @Author   : Zhangyu
# @Email    : zhangycqupt@163.com
# @File     : flush_service.py
# @Software : PyCharm
# @Desc     :
"""

import os
import sys
from threading import Thread

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


def flush_thread_factory(module, sub_module, query):
    if module == "test":
        if sub_module == "test":
            pipe = TestDataProcessPipeline()
            t = Thread(target=generate_tasks,
                       args=(count_query, query, pipe, fetch_data_from_mysql_db_by_job_ids, insert_data_info))
            return t
        elif sub_module == "test_1":
            pass
    elif module == "test1":
        if sub_module == "test":
            pipe = TestDataProcessPipeline()
            t = Thread(target=generate_tasks,
                       args=(count_query, query, pipe, fetch_data_from_mysql_db_by_job_ids, insert_data_info))
            return t

    return None


@app.route("/cf-nlp-py/data_service/<string:module>/<string:module>")
def flush_main(module, sub_module):
    start_time = request.args.get('start_time', '2020-07-12')
    end_time = request.args.get('end_time', '2020-08-12')
    job_ids = request.args.get('job_ids', '').split(',')

    query = {
        'start_time': start_time,
        'end_time': end_time,
        'job_ids': job_ids
    }
    t = flush_thread_factory(module, sub_module, query)
    if t:
        t.setDaemon(True)
        t.start()
        return jsonify({"resultCode": "0", "resultMessage": "请求成功，正在重刷数据"})
    return jsonify({"resultCode": "0", "resultMessage": "请求module未匹配"})


@app.route("/cf-nlp-py/data_service/test")
def flash_from_mysql_db():
    start_time = request.args.get('start_time', '2020-07-12')
    end_time = request.args.get('end_time', '2020-08-12')
    job_ids = request.args.get('job_ids', '').split(',')

    query = {
        'start_time': start_time,
        'end_time': end_time,
        'job_ids': job_ids
    }

    pipe = TestDataProcessPipeline()
    t = Thread(target=generate_tasks,
               args=(count_query, query, pipe, fetch_data_from_mysql_db_by_job_ids, insert_data_info))
    t.setDaemon(True)
    t.start()
    return jsonify({"resultCode": "0", "resultMessage": "请求成功，正在重刷数据"})


def stop_flush():
    job_ids = request.args.get('job_ids', '').split(',')
    all, suc = stop_tasks(job_ids)
    return jsonify({"resultCode": "0", "resultMessage": "取消成功：{%d}，取消失败{%d}" % (suc, all - suc)})


if __name__ == "__main__":
    os.environ["ENV"] = "dev"
    if len(sys.argv) == 2:
        os.environ["env"] = sys.argv[1]

    res = os.path.abspath(__file__)  # 获取当前文件绝对路径
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(res)))  # 获取当前文件的上三级目录
    sys.path.insert(0, base_path)

    from cfnlp.process.concurrent_flush import generate_tasks, stop_tasks
    from cfnlp.process.db_query import count_query, fetch_data_from_mysql_db_by_job_ids, insert_data_info
    from cfnlp.process.filed_processor import TestDataProcessPipeline

    # host="0.0.0.0" 加上允许远程访问
    app.run(debug=True, threaded=False, processes=1, host="0.0.0.0", port=8100)
