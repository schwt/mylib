#!/bin/bash
#!encoding:utf-8

HADOOP="/home/idm/clients/hadoop-HY/bin/hadoop"

function timestamp {
    date +%s 
}
function timediff {
    old=$1
    new=`timestamp`
    dif=$[$new - $old]
    echo $dif
}
function datetime {
    date +"[%Y-%m-%d %H:%M:%S]"
}

function ndate {
    n=$1
    date -d "$n days ago" +"%Y-%m-%d"
}

function date_range {
    n=$1
    for i in `seq 1 $n`; do
        date -d "$i days ago" +"%Y-%m-%d"
    done
}

function split {
    string=$1
    delimiter=$2
    OLD_IFS="$IFS" 
    IFS="," 
    arr=($string) 
    IFS="$OLD_IFS" 
    echo ${arr[@]} 
}

function date_range_filter {
    days=$1
    black_list=$2
    for i in `seq 1 $days`; do
        d=`date -d "$i days ago" +"%Y-%m-%d"`
        if ! [[ $black_list =~ $d ]]; then
            echo $d
        fi  
    done
}

# return: list1 - list2
# list 要用连接符链接
# `list_not_in "11,22,33,44" "yy,11,22,aa" ","` => "33 44"
function list_not_in {
    delimiter=$3 
    src_list=`split $1 ${delimiter}`
    black_list=$2
    for s in ${src_list[@]}; do
        if ! [[ $black_list =~ $s ]]; then
            echo $s
        fi  
    done
}

# 连接数组, join "," ${array}
function join() {
    local sep="$1"
    shift
    local dst="$1"

    shift
    for s in "$@"
    do
        dst=${dst}${sep}${s}
    done
    echo "$dst"
}

# date_range 10

