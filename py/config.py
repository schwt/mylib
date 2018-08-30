#!/usr/bin/env python
#!encoding:utf-8
import ConfigParser

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

