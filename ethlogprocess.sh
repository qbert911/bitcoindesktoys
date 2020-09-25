#!/bin/bash
#month=( $(cut -d ',' -f1 uniswaplog.csv ) )
#day=( $(cut -d ',' -f2 uniswaplog.csv ) )
time=( $(cut -d ',' -f3 /home/pi/uniswaplog.csv ) )
value=( $(cut -d ',' -f4 /home/pi/uniswaplog.csv ) )

function apr (){
x=$((-1))-$1
b1=$(echo "${time[-1]:0:2} - ${time[$x]:0:2}" | bc)
if [[ "$b1" -le "0" ]];then b1=$(($b1 + 24));fi
if [[ "$b1" -ne "$1" ]];then echo -n " DATA ERROR $b1 is not $1 ";fi
b2=$(echo "${value[-1]} - ${value[$x]}" | bc)
b3=$(printf "%.4f\n" "$(echo $b2 / $b1 *24 | bc -l)")
b4=$(printf "%.2f\n" "$(echo $b2 / $b1 *24*365 / ${value[-1]:0:2} | bc -l)")
#echo "${time[-1]:0:2} - ${time[$x]:0:2} = $b1 hours we earned $b2 which is $b3 per day which is $b4% APR"
echo -n "(${b1}hr/$b4%)"
}


b6=$(printf "%.2f\n" "$(echo "${value[-1]} - ${value[-2]}" | bc)")
echo -en " [ \e[38;5;086m$b6\e[0m ] "
apr 1
apr 6
apr 12
apr 18
apr 24
