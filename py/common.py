#!/usr/bin/env python
#!encoding:utf-8
import os
from datetime import datetime as dt

def get_dir_files(dir_src):
    return sorted(filter(lambda x: x[0] != ".", os.listdir(dir_src)))

def inverse_dict(dic):
    ivs = {}
    for k,v in dic.iteritems():
        values = ivs.get(v)
        if values:
            values.add(k)
        else:
            ivs[v] = {k}
    return ivs

def atoi(s):
    try:
        return int(s)
    except:
        return -1

class Flag:
    @classmethod
    def set_flag(self, flag_file, x, y=-1):
        import time
        if y == -1:
            with open(flag_file,'w') as wf:
                wf.write(str(x))
        else:
            while True:
                flag = int(file(flag_file).readline().strip())
                if flag == y:
                    with open(flag_file,'w') as wf:
                        wf.write(str(x))
                    break
                else:
                    time.sleep(5)
    @classmethod
    def check_flag(self, flag_file, x):
        import time
        try:
            flag = int(file(flag_file).readline().strip())
        except:
            flag = x+1
        return flag == x

    @classmethod
    def waite_flag(self, flag_file, x=1):
        import time
        while True:
            try:
                flag = int(file(flag_file).readline().strip())
            except:
                flag = x+1
            if flag == x:
                return True
            else:
                time.sleep(5)

class Title:
    # for print like: __________ TITLE __________
    def __init__(self):
        self._dline = "=========="
        self._sline = "__________"

    def t1(self, s):
        return "\n{0} {1} {0}".format(self._dline, s)

    def t2(self, s):
        return "{0} {1} {0}".format(self._sline, s)

    def t3(self, s):
        return "\t{0} {1} {0}".format(self._sline, s)

class Title2:
    dline = "=========="
    sline = "__________"

    @classmethod
    def t1(self, s):
        print "\n{0} {1} {0}".format(self.dline, s)

    @classmethod
    def t2(self, s):
        print "{0} {1} {0}".format(self.sline, s)

    @classmethod
    def t3(self, s):
        print "\t{0} {1} {0}".format(self.sline, s)


class Evaluate:
    # model evaluate
    @classmethod
    def auc(self, ll):
        # get auc
        # ll: [ [score, y], [], ...]
        m, n, sq = 0, 0, 0.
        ll.sort(key = lambda x: -x[0])
        for score, y in ll:
            if y == 1:
                n += 1
            if y == 0:
                sq += n
                m += 1
        if m == 0  or n == 0:
            print "@ error auc"
            return 0.
        return sq / (m * n)

def format_second(x):
    seconds = x % 60
    x = x / 60
    minutes = x % 60
    hours = x / 60
    return "%s:%02d:%02d" %  (hours, minutes, seconds)

def running_time(func):
    import time
    def wrapper(*args, **kv):
        time_start = int(time.time())
        ret = func(*args, **kv)
        time_end = int(time.time())
        dter = str(dt.now())[:-7]
        print "[%s][%s] use time: %s" % (dter, func.__name__, format_second(time_end - time_start))
        return ret
    return wrapper
