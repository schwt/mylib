#!/bin/bash
#!encoding:utf-8

HADOOP_DIR="/home/idm/clients/hadoop-HY"
HADOOP="${HADOOP_DIR}/bin/hadoop"
HADOOP_STREAM="${HADOOP_DIR}/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar"

beeline='/home/idm/clients/hive-1.2.1/bin/beeline -u "jdbc:hive2://hadoop1232.hz.163.org:2181,hadoop1233.hz.163.org:2181,hadoop1234.hz.163.org:2181/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2;principal=hive/hadoop1236.hz.163.org@HADOOP.HZ.NETEASE.COM"'

beelinet='/home/idm/clients/hive-1.2.1/bin/beeline -u "jdbc:hive2://hadoop1232.hz.163.org:2181,hadoop1233.hz.163.org:2181,hadoop1234.hz.163.org:2181/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2;principal=hive/hadoop1236.hz.163.org@HADOOP.HZ.NETEASE.COM" --outputformat=tsv2 --showHeader=false'
## export beelinet='/home/idm/clients/hive-1.2.1/bin/beeline -u "jdbc:hive2://hadoop1232.hz.163.org:2181,hadoop1233.hz.163.org:2181,hadoop1234.hz.163.org:2181/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2;principal=hive/_HOST@HADOOP.HZ.NETEASE.COM" --outputformat=tsv2 --showHeader=false'


