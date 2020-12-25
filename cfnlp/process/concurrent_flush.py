#!/usr/bin/env python
# coding:utf-8
"""
# @Time     : 2020-08-12 19:44
# @Author   : Zhangyu
# @Email    : zhangycqupt@163.com
# @File     : concurrent_flush.py
# @Software : PyCharm
# @Desc     :
"""
import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from peewee import fn
from tqdm import tqdm

from cfnlp.model.peewee_models import TestData
from cfnlp.stable.murmurhash import murmurhash
from cfnlp.tools.logger import logger

future_queue = {}
executor = ThreadPoolExecutor(20)
task_stop_flags = {}

lock_arr = {}
for i in range(0, 80):  # 冲突多速度慢，可设置大一点
    lock_arr[i] = Lock()


def process_task(query, pipe, db_query, stop_flag):
    job_ids = query.get("job_ids")
    page_num = query.get("page_num")
    page_size = query.get("page_size")
    start_time = query.get("start_time")
    end_time = query.get("end_time")
    task_stop_flags[stop_flag] = False
    result = []

    batch_data = db_query(job_ids, start_time, end_time, page_num, page_size)
    for d in tqdm(batch_data.dicts(), des="offset %s" % page_num):
        try:
            data = json.loads(d.get("data"))
        except Exception:
            continue
        cur_data = pipe.process_data(data)
        if cur_data and len(cur_data) > 0:
            try:
                result.append(data)
            except Exception as e:
                logger.error("flush insert db error, exception %s, offset - %s" % (e, page_num))
    return "offset %s completed" % page_num, result


def generate_tasks(count_query, query_params, pipe, db_query, db_operator):
    job_ids = query_params.get("job_ids")
    page_size = int(query_params.get("page_size", "200"))  # 表格字段文本内容太大，不适合一页取太多条记录，多线程时内存将加载太多记录
    start_time = query_params.get("start_time")
    end_time = query_params.get("end_time")

    count_query_new = count_query(job_ids, start_time, end_time)
    count = count_query_new.scalar()
    logger.info("sum count for test data flush: %s" % count)

    key = "-".join(job_ids)
    future_queue[key] = []
    for i in range(0, count, page_size):
        new_query = query_params.copy()
        new_query["page_size"] = page_size
        new_query["page_num"] = int(i / page_size)
        future_queue[key].append(executor.submit(process_task, new_query, pipe, db_query, db_operator))
        logger.info("new future task is generated: offset - {}, page_size - {}".format(i, page_size))

    save_queue = []
    for f in as_completed(future_queue[key], timeout=7200):
        info, cur_result = f.result
        logger.info(f.result())
        # 假设 db_model parameters
        db_model = TestData
        save_queue.append(executor.submit(save_to_db_sup, cur_result, db_operator, info, db_model))

    for f in as_completed(save_queue):
        logger.info(f.result)

    logger.info("test topic completed.")
    future_queue[key] = []
    try:
        task_stop_flags.pop(key)
    except Exception:
        logger.info("stop flag key not found")


def save_to_db_sup(cur_result, db_operator, info, db_model):
    for item in tqdm(cur_result, desc="insert data to table - %s" % info):
        db_unique_key = item.get("code", "")
        key_hash = murmurhash(db_unique_key) % 80
        lock = lock_arr[key_hash]
        try:
            if db_model.__name__ == "test":
                # 同一条数据，线程加锁，保证冲突时只有一个线程在对该条数据进行操作
                # 非原子操作
                with lock:
                    db_operator(item)
            elif db_model.__name__ == "test1":
                # 同一条数据，线程加锁，保证冲突时只有一个线程在对该条数据进行操作
                # 原子操作（数据库层操作
                with lock:
                    db_model.insert(item).on_conflict_replace().execute()
            elif db_model.__name__ == "test2":
                # 解决冲突，但非原子操作
                try:
                    count = db_model.select(fn.COUNT(db_model.id)).where(db_model.code == item["code"]).scalar()
                    if count == 0:
                        db_model.insert(item).execute()
                    else:
                        db_model.update(item).where(db_model.code == item["code"]).execute()
                except Exception as e:
                    logger.error(e)
            else:
                # 数据库的系统时间可能有偏差
                item["create_time"] = datetime.datetime.now()
                # 多线程同时操作同一条数据时会报错
                db_model.insert(item).on_conflict_replace().execute()
        except:
            logger.info("dup key conflict, ignore the data")
    return "insert data in to table" + info + "completed."


def stop_tasks(job_ids):
    key = "-".join(job_ids)
    task_stop_flags[key] = True
    task_num = len(future_queue[key])
    suc_cnt = 0
    for f in future_queue[key]:
        f.cancel()
        if f.isCancelled():
            suc_cnt += 1
    future_queue[key] = []
    return task_num, suc_cnt
