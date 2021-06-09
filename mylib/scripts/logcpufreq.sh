#/bin/bash

if [ $# -ne 2 ]
then
    printf "Usage: ./$0 \$freq_limit(sec) \$count_limit (limit: LLMAX) \n"
    exit -1
fi

freq_limit=$1
count_limit=$2

timestamp=`date +"%Y%m%d_%H%M%S"`
thread_arr=(16 8 4 2 1)

runomp(){
    echo $FUNCNAME
    echo "numamax: " $numamax

    numamax=$(($1-1))

    if [ $1 -eq 0 ]
    then
        numactl -C 0 ./omp.out
    else
        numactl -C 0-$numamax ./omp.out $count_limit $1
    fi
}


logcpufreq(){
    echo $FUNCNAME

    f_name=log_$1\_threads
    touch $f_name\.txt
    > $f_name\.txt

    log_cnt=0
    while [ $log_cnt -le 20 ]
    do
        cat /proc/cpuinfo | grep "MHz" | head -1 | awk -F: '{ print $2 }' 2>&1 | tee -a $f_name.txt
        sleep $freq_limit
        log_cnt=$(($log_cnt+1))
    done
}

for thread in ${thread_arr[@]}
do
    runomp $thread &
    logcpufreq $thread &
    wait
done
