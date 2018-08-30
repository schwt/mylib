#!/usr/bin/env python
#!encoding:utf-8
import os
import signal
from functools import wraps
from datetime import datetime as dt
import datetime

class TimeRange:
    @classmethod
    def nDate(n):
        # n天前的日期
        return str(datetime.date.today() - datetime.timedelta(days=n))
    @classmethod
    def nDateList(n):
        # n天内的日期
        return [nDate(n) for n in xrange(n)]

class Timer:
    # log time consuming
    def __init__(self):
        self._dt0 = dt.now()
        print self._dt0.strftime('[%Y-%m-%d %H:%M:%S]')

    def init(self, info=""):
        self._dt0 = dt.now()
        print self._dt0.strftime('[%Y-%m-%d %H:%M:%S] ')+info

    def logt(self):
        dt_t = dt.now()
        dif = str(dt_t - self._dt0).split('.')[0]
        self._dt0 = dt_t
        print dt_t.strftime('[%Y-%m-%d %H:%M:%S] ') + dif

class Timer2(object):
    import arrow
    def __init__(self, prefix="", verbose=True, log=None):
        self.verbose = verbose
        self.prefix = prefix
        self.log = log

    def __enter__(self):
        self.start = arrow.now()
        return self

    def __exit__(self, *args):
        self.end = arrow.now()
        self.secs = self.end - self.start
        self.msecs = self.secs.total_seconds()
        if self.verbose:
            if not self.log:
                print '%s elapsed time: %f s' % (self.prefix, self.msecs)
            else:
                self.log.info('%s elapsed time: %f s' % (self.prefix, self.msecs))

def running_time(func):
    import arrow
    def wrapper(*args, **kv):
        time_start = arrow.now().timestamp
        ret = func(*args, **kv)
        time_end = arrow.now().timestamp
        dter = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        print "[%s][%s] use time: %s" % (dter, func.__name__, format_second(time_end - time_start))
        return ret
    return wrapper


def overtime(seconds):
    # 装饰器：超时则退出
    def myHandler(signum, frame):
        print("job overtime %ds! exit." % seconds)
        exit()
    def func_wrapper(func):
        @wraps(func)
        def return_wrapper(*args, **wkargs):
            signal.signal(signal.SIGALRM, myHandler)
            signal.alarm(seconds)
            re = func(*args, **wkargs)
            return re
        return return_wrapper
    return func_wrapper


# 时间分桶相关，以桶内最大时间+1s为标记(前闭后开区间)
# "20151215-04:20": [04:10:00, ..., 04:19:59]
class TimeBin:
    import arrow
    def __init__(self, width, form = "YYYYMMDD-HH:mm"):
        # 桶宽度(分钟)
        self.width  = width
        self.s_form = form
        self.delay  = 3 * self.width * 60 #保留数据源延迟时间(3min)

    def time2bin(self, ut):
        # unix time to a bin
        ar = self.arrow.get(ut + 60*self.width).to('local')
        dm = ar.minute - ar.minute % self.width
        ar = ar.replace(minute = dm)
        return ar.format(self.s_form)

    def bin2time(self, s):
        # bin名对应时间(桶内最右时刻)
        then = self.arrow.get(s+" +08:00", 'YYYYMMDD-HH:mm ZZ')
        return then.timestamp

    def form(self, utime, form="YYYYMMDD-HH:mm"):
        return self.arrow.get(utime).to('local').format(form)

    def get_last_time(self, dir, hours = 5):
        # 查找目录下最新时间桶，但不早于 hours 个小时前
        begin = self.arrow.get(self.arrow.now().timestamp -
                hours*3600).to('local').timestamp - self.delay
        file_list = os.listdir(dir)
        try:
            lasts = file_list[0]
            for name in file_list:
                if len(name) != len(self.s_form): continue
                then = self.bin2time(name)
                begin = max(begin, then)
                lasts = max(lasts, name)
            print 'last file:', lasts
        except:
            pass
        return begin
    def del_overtime(self, dir, overdays):
        def check_overtime(a, b):
            return b-a > 86400*overdays
        file_list = os.listdir(dir)
        for name in file_list:
            if len(name) != len(self.s_form):
                continue
            then = self.bin2time(name)
            if check_overtime(then, self.arrow.now().timestamp):
                try:
                    os.remove(dir + '/' + name)
                except:
                    pass

    def get_bins(self, ut, end = -1):
        import time
        # 返回从ut到目前(或end)所有的时间桶（最近的若不完整则不算）
        bins = set()
        flag = False
        if end == -1:
            end = self.arrow.now().timestamp - self.delay
            flag = True
        while ut < end:
            bins.add(self.time2bin(ut))
            ut += self.width*50
        if not bins:
            if flag:
                time.sleep(self.width*50)
                return self.get_bins(ut)
            else:
                return [], ut
        else:
            bins = list(bins)
            bins.sort()
            return bins, self.bin2time(bins[-1])

    def bin_boundary(self, bin):
        # 返回时间桶对应的开始、结束时间(unix time)
        tail = self.bin2time(bin)
        head = tail - self.width * 60
        return head, tail-1

