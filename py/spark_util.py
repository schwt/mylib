#!/usr/bin/env python
# encoding: utf-8
from operator import add

# 生成几小时内的所有hdfs文件名列表
def fileList(path, hours):
    import arrow
    unow = arrow.now().timestamp
    ubegin = int(unow - hours * 3600)
    files = []
    for ut in xrange(ubegin, unow, 60):
        t = arrow.get(ut).to('local')
        if t.minute % 5 != 0: continue
        path1 = t.format('YYYYMMDDHH')
        path2 = t.format('YYYYMMDDHHmm')
        files.append(path + '/' + path1 + '/' + path2+"/*")
    print "gener files:", len(files)
    for f in files:
        print f
    return files

# 把多个文件加入同一个rdd
def files2rdd(sc, file_list):
    fileRDD = sc.textFile(file_list[0])
    cnt = 0
    for f in file_list[1:]:
        try:
            fileRDD = fileRDD.union(sc.textFile(f))
            cnt +=1
        except:
            pass
    print '######################'
    print 'effect logs:', cnt
    print '######################'
    print '\n\n\n'
    return fileRDD

def files2functionedRDD(sc, func, file_list):
    fileRDD = func(sc, sc.textFile(file_list[0]))
    cnt = 0
    for f in file_list[1:]:
        try:
            fileRDD = fileRDD.union(func(sc, sc.textFile(f)))
            cnt +=1
        except:
            pass
    print '######################'
    print 'effect logs:', cnt
    print '######################'
    print '\n\n\n'
    return fileRDD.coalesce(30)

# Guangzhou order/click/impression的通用解析器，返回(uid,mid,lable)
def parseGZmall_log(sc, src_rdd, label, rate_sample):
    cnt = sc.accumulator(0)
    def parse(line):
        sep = line.strip().split(",")
        try:
            uid = int(sep[3])
            mall = int(sep[13].split("_")[0])
            if uid >0 and 100000 < mall < 1000000:
                return (uid, mall, label)
            else:
                return ()
        except:
            return ()
    re = src_rdd.sample(False, rate_sample, 0) \
            .map(lambda line: parse(line)) \
            .filter(lambda x: len(x)>0) \
            .cache()
    return re

# Guangzhou order/click/impression的通用解析器，返回(uid,mid,cnt)
def parseGZmall_log2(sc, log_file, sample_rate):
    def parse(line):
        sep = line.strip().split(",")
        try:
            uid = int(sep[3])
            mall = int(sep[13].split("_")[0])
            if uid >0 and 100000 < mall < 1000000:
                return ((uid, mall), 1)
            else:
                return ()
        except:
            return ()
    re = sc.textFile(log_file) \
            .sample(False, sample_rate, 0) \
            .map(lambda line: parse(line)) \
            .filter(lambda x: len(x)>0) \
            .reduceByKey(add) \
            .map(lambda x: (x[0][0],x[0][1],x[1]))
    return re

def get_hdfs_end_date(path, n=8):
    import os
    cmd = """ 
       hadoop fs -ls %s | awk '{if (NF==8) {len=length($NF); print substr($NF, len-%d+1)}}'
          """ % (path, n)
    re = os.popen(cmd).read().strip().split('\n')
    return sorted(filter(lambda x: x!="", re), reverse=True)

def get_days_range(days):
    import arrow
    ut = arrow.now().timestamp
    res = []
    for i in xrange(days):
        dt = arrow.get(ut).to('local').format("YYYYMMDD")
        res.append(dt)
        ut -= 24*3600
    return sorted(res, reverse=True)
