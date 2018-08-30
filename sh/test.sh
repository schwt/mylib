#!/bin/bash
source ./directory.sh
source ./hdfs.sh
source ./utils.sh

# d=`list_not_in "11,22,33,44" "yy,11,22,aa" ","`
# echo $d
# exit 0

function test_hdfs {
    path="hdfs://hz-cluster6/user/kaolarec/hive_db/kaola_rec_algo.db/wyb_new_action_goods/"
    dates=`get_hdfs_dates ${path}`
    echo ${dates[@]}
}

function test_dir {
    path="/home/idm/data/wyb/data/action_stat_goods/daily"
    dates=`get_dir_files $path`
    echo ${dates[@]}
}

d1=`test_hdfs`
d1=`join "," $d1`
echo "1"
echo ${d1[@]}


d2=`test_dir`
d2=`join "," $d2`
echo "2"
echo ${d2[@]}

echo "2"
d3=`list_not_in ${d1[@]} ${d2[@]} ","`
echo ${d3}
