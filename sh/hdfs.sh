#!/bin/bash
#encoding:utf-8

function get_hdfs_dates {
    dir=$1
    hadoop fs -ls $dir | awk -F "day=" '{if (NF==2) {print $2}}'
}

# 判断hdfs目录是否存在
function hdfs_exist {
    path=$1
    `${HADOOP} fs -test -e ${path}`
    if [ $? -eq 0 ]; then
        echo 1
    else
        echo 0
    fi
}
function hdfs_wait {
    path=$1
    wait_times=12
    if [[ -n $2 ]]; then
        wait_times=$2
    fi
    ret=0
    for i in `seq 1 $wait_times`; do
        check=`hdfs_exist $path`
        if [[ "$check" == "1" ]]; then
            ret=1
            break
        else
            sleep 10m
            continue
        fi
    done
    echo $ret
}
