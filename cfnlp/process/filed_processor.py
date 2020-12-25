#!/usr/bin/env python
# coding:utf-8
"""
# @Time     : 2020-08-12 18:06
# @Author   : Zhangyu
# @Email    : zhangycqupt@163.com
# @File     : filed_processor.py
# @Software : PyCharm
# @Desc     :
"""
from abc import ABCMeta, abstractmethod
from cfnlp.tools.logger import logger


class AbstractFiledProcessor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, input):
        cur_result = {}
        try:
            data_without_process, data_to_process = self.parse_input(input)
            cur_result.update(data_to_process)
            data_processed = self.inner_process(data_to_process)
            cur_result.update(data_processed)
        except Exception as e:
            logger.error("process data error: %s" % str(e))
        return self.filter_output(cur_result)

    @abstractmethod
    def parse_input(self, input):
        pass

    @abstractmethod
    def inner_process(self, input):
        pass

    @abstractmethod
    def filter_output(self, input):
        pass


class TestDataProcessPipeline(object):

    def __init__(self):
        self.processors = []
        self.processors.append(NullFiledProcessor())

    def process_data(self, data):
        cur_data = data
        for p in self.processors:
            cur_data = p.process(cur_data)
        return cur_data


class NullFiledProcessor(AbstractFiledProcessor):

    def __init__(self):
        self.using_key = {"key1", "key2"}

    def parse_input(self, input):
        data_without_process = {}
        data_to_process = {}
        for k, v in input.items():
            if k in self.using_key:
                data_to_process[k] = v

        return data_without_process, data_to_process

    def inner_process(self, input):
        if input.get("key1", "") == "NULL":
            input["key1"] = ""
        if input.get("key2", "") == "NULL":
            input["key2"] = ""
        return input

    def filter_output(self, input):
        return input
