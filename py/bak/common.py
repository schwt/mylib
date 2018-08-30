#!/usr/bin/env python
#!encoding:utf-8
import cPickle
from datetime import datetime as dt  
import arrow

class config: 
    @classmethod
    def init_config(self, confile = 'config.ini'):
        import ConfigParser
        cf = ConfigParser.ConfigParser()
        cf.read(confile)
        config = {}
        for k in cf.sections():
            config[k.lower()] = {}
            for v in cf.items(k):
                try:
                    config[k.lower()][v[0].lower()] = eval(v[1])
                except:
                    config[k.lower()][v[0].lower()] = v[1]
    
            for key,value in config[k.lower()].items():
                try:
                    subname = re.findall('\$(.*)\$', value)[0]
                    config[k.lower()][key.lower()] = re.sub('\$'+subname+'\$', config[k.lower()][subname.lower()], value)
                except:
                    pass
        return config

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

def format_second(s): 
    # 将秒数转换为 HH:mm:ss (有必要则再加天数)
    t = arrow.get(s).format("HH:mm:ss")
    d = int(s/24/3600)
    if d > 0:
        t = "%02ddays " % d + t 
    return t
def format_timestamp(t, form="YYYY-MM-DD HH:mm:ss"):
    return arrow.get(t).to("local").format(form)

class Timer:
    # log time consuming
    def __init__(self):
        self._dt0 = arrow.now().timestamp
    
    def init(self, info=""):
        self._dt0 = arrow.now().timestamp
    
    def logt(self):
        dt_t = arrow.now().timestamp
        dif = int(dt_t - self._dt0)
        self._dt0 = dt_t
        slog = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        print '[%s] %d' % (slog, dif)

    def used_time(self):
        dt_t = arrow.now().timestamp
        dif = int(dt_t - self._dt0)
        self._dt0 = dt_t
        return format_second(dif)

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


class mypickle: 
    @classmethod
    def dump(self, buff, dst, b=False): 
        with open(dst, 'w') as wf: 
            cPickle.dump(buff, wf, b) 

    @classmethod
    def load(self, src): 
        with open(src, 'r') as rf: 
            return cPickle.load(rf) 

def running_time(func): 
    import arrow 
    def wrapper(*args, **kv): 
        time_start = arrow.now().timestamp  
        ret = func(*args, **kv)
        time_end = arrow.now().timestamp  
        dt = arrow.now().format("YYYY-MM-DD HH:mm:ss") 
        print "[%s][%s] use time: %s" % (dt, func.__name__, format_second(time_end - time_start)) 
        return ret 
    return wrapper 

class Timer2(object):

    def __init__(self, prefix="", verbose=True, log=None):
        self.verbose = verbose
        self.prefix = prefix
        self.log = log

    def __enter__(self):
        import arrow
        self.start = arrow.now()
        return self

    def __exit__(self, *args):
        import arrow
        self.end = arrow.now()
        self.secs = self.end - self.start
        self.msecs = self.secs.total_seconds()
        if self.verbose:
            if not self.log:
                print '%s elapsed time: %f s' % (self.prefix, self.msecs)
            else:
                self.log.info('%s elapsed time: %f s' % (self.prefix, self.msecs))

class myLog():
    def __init__(self, date=1, time=1, module=1, funcName=1, lineno=1, flog=None, justify=25):
        self.sdate     = date
        self.stime     = time
        self.smodule   = module 
        self.sfuncName = funcName 
        self.smodule   = module
        self.slineno   = lineno
        self.out_file  = flog
        self.justify   = justify  # 对齐与否(负数左，正数右)

    def info(self, msg=''):
        import sys, arrow
        now = arrow.now()
        frame = sys._getframe().f_back
        s  = ''
        dt, name = '', ''
        if self.sdate:
            dt += now.format('YYYY-MM-DD')
        if self.stime:
            dt += now.format(' HH:mm:ss')
        if dt: 
            dt = '[%s]' % dt  
        if self.smodule:
            name += '%s' % self._module_name(frame)
        if self.sfuncName:
            if name: name += '.' 
            name += '%s' % frame.f_code.co_name
        if name:
            s += '[%s]' % name 
        if self.slineno:
            s += '[%s]' % frame.f_lineno
        if self.justify > 0:
            s = s.rjust(self.justify)
        elif self.justify < 0:
            s = s.ljust(-self.justify)
        rst = dt + s + ' ' + str(msg)
        print rst
        if self.out_file:
            with open(self.out_file, 'a') as wf:
                wf.write(rst + "\n")

    def _module_name(self, frame):
        import os
        pathname = frame.f_code.co_filename
        filename = os.path.basename(pathname)
        module   = os.path.splitext(filename)[0]
        return  module

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
        import os
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
        import os
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
        # 返回从ut到目前(或end)所有的时间桶（最近的若不完整则不算）
        import time
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

def overtime(seconds):
    # 装饰器：超时则退出
    import signal
    from functools import wraps
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

