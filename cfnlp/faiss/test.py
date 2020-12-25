#!/usr/bin/env python
# coding:utf-8
"""
# @Time     : 2020-07-27 14:29
# @Author   : Zhangyu
# @Email    : zhangycqupt@163.com
# @File     : gaode_interface.py
# @Software : PyCharm
# @Desc     :
"""

import numpy as np
import faiss


d = 64                           # dimension
nb = 100000                      # database size
nq = 10000                       # nb of queries
np.random.seed(1234)             # make reproducible
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.
xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.


# # IndexFlatL2
# index = faiss.IndexFlatL2(d)   # build the index
# print(index.is_trained)
# index.add(xb)                  # add vectors to the index
# print(index.ntotal)
#
# # IndexIVFFlat
# k = 4                          # we want to see 4 nearest neighbors
# D, I = index.search(xb[:5], k)     # actual search
# print(I[:5])                   # neighbors of the 5 first queries
# print(D[-5:])                  # neighbors of the 5 last queries
#
# nlist = 100 # 单元格数
# k = 4
# quantizer = faiss.IndexFlatL2(d)  # the other index  d是向量维度
# index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
# # here we specify METRIC_L2, by default it performs inner-product search
# assert not index.is_trained
# index.train(xb)
# assert index.is_trained
# index.add(xb)                  # add may be a bit slower as well
# D, I = index.search(xb[:5], k)     # actual search
# print(I[-5:])                  # neighbors of the 5 last queries
# print(D[-5:])
#
# index.nprobe = 10        # 执行搜索访问的单元格数（nlist以外）      # default nprobe is 1, try a few more
# D, I = index.search(xb[:5], k)
# print(I[-5:]) # neighbors of the 5 last queries
# print(D[-5:])

# IndexIVFPQ
nlist = 100
m = 8                             # number of bytes per vector
k = 4
quantizer = faiss.IndexFlatL2(d)  # this remains the same
index = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)  # 8 specifies that each sub-vector is encoded as 8 bits
index.train(xb)
index.add(xb)
D, I = index.search(xb[:5], k) # sanity check
print(I)
print(D)

index.nprobe = 10              # make comparable with experiment above
D, I = index.search(xq, k)     # search
print(I[-5:])
print(D[-5:])