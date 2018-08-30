#!/usr/bin/env python
#!encoding:utf-8
import cPickle 
import ConfigParser
import time from datetime import datetime as dt  

class config: 
    @classmethod
    def init_config(self, confile = 'config.ini'):
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
        # check flag in flag_file
        # if y == -1:  
        #   set flag = x 
        # if y != -1:  
        #   if flag==y:  
        #       set flag = x 
        #   else:
        #       waite 
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
                    time.sleep(1) 
        
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
        

class Title:
    # for print like: __________ TITLE __________ 
    def __init__(self):
        self._dline = "==========" 
        self._sline = "__________" 

    def t1(self, s): 
        return "{0} {1} {0}".format(self._dline, s) 

    def t2(self, s): 
        return "{0} {1} {0}".format(self._sline, s) 

    def t3(self, s): 
        return "\t{0} {1} {0}".format(self._sline, s) 


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

