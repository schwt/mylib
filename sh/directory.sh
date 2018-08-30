#!/bin/bash
#encoding:utf-8

########## NOTE ########## 
#  不支持软链路径
########################## 

# 目录下文件列表，不递归，不包含子目录
function get_dir_files {
    dir=$1
    for file in $(ls $dir); do
        [ -f $dir/$file ] && echo $file
    done
}

function date_range {
    n=$1
    for i in `seq 1 $n`; do
        date -d "$i days ago" +"%Y-%m-%d"
    done
}

# 判断x是否在数组arr中： if check_in $x "$arr"
# TODO 对明文定义的数组无效
function check_in {
    x=$1
    array="$2"
    if [[ "${array[@]}" =~ $x ]]; then
        return 0
    else
        return 1
    fi
}

function main {
    days=`date_range 10`
    d1="2018-01-02"
    d2="2017-01-02"
    if check_in $d1 "$days"; then echo "in"
    else echo "not in"; fi
    if check_in $d2 "$days"; then echo "in"
    else echo "not in"; fi
}

#### for test:
# main

