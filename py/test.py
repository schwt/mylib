#!/usr/bin/python
#encoding:utf-8
import pymmh3 as mmh

arr = ['brand_id@1007', 'category_id@9990', 'item_discount', "item_discountx", "item_dis213count", "item_discount7"]

base = 10000000

for s in arr:
    v = mmh.hash128(s)
    print "%s\t%s" % (v, v%base)

