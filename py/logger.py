#!/usr/bin/env python
#!encoding:utf-8
from datetime import datetime as dt
import sys, arrow
import os

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
        pathname = frame.f_code.co_filename
        filename = os.path.basename(pathname)
        module   = os.path.splitext(filename)[0]
        return  module

