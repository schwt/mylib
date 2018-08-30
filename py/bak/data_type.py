#!/usr/bin/env python
#!encoding:utf-8

def inverse_dict(dic):
    ivs = {}
    for k,v in dic.iteritems():
        values = ivs.get(v)
        if values:
            values.add(k)
        else:
            ivs[v] = {k}
    return ivs

def atoi(s, default=0):
    try:
        return int(s)
    except:
        return default

