#!/bin/bash
# shellcheck disable=SC2004
eval 'ulimit -S -s 16384' #to help prevent segfault errors when running show_digitsmove
hasunicornhat=$(cat /home/pi/config.json | jq '.invert_unicornhat')
echo -e "Watching BTC price movements..."
while : ;do
  usdraw=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
  if echo "$usdraw" | grep -q '{"usd":'  ;then            #data scrape was successful
    usdreading=$(echo "$usdraw" |jq -r '.bitcoin.usd')
    if [ -z "$usdreading" ] || [[ "$usdreading" = "null" ]] || [[ "$usdreading" = "0" ]];then usdreading=$lastreading;fi #in case of timeout
    usdreading=$(printf '%04.0f' "$usdreading")
  else
    usdreading=$lastreading; echo -en "x"; sleep 30       #data scrape unsuccessful
  fi
  if  [[ "$usdreading" = "$lastreading" ]];then    #price hasnt changed
        echo -en "."
  else                                                    #time to report a change in price
    if [[ "$usdreading" > "$lastreading" ]];then
      changeup=$(($change+1))
      change=$(( $changeup > 10 ? 10 : $changeup ))
    else
      changeup=$(($change-1))
      change=$(( $changeup < -10 ? -10 : $changeup ))
    fi
    if [[ "${#lastreading}" = "0" ]];then
      START=$(date +%s)
      eval "/home/pi/bitcoindesktoys/show_digitsmove.py $usdreading $usdreading 0" &
      echo -en "\$$usdreading       ["
    else
      echo -e "] $(( $(date +%s) - $START )) seconds ($(date +%X))"
      START=$(date +%s)
      while [[ "$(( $(date +%_S) + 1 ))" -ne "60" ]];do sleep 0.05;done #sync multiple units
      pdfull="$(printf '%+04.0f' "$(echo $usdreading - $lastreading | bc )" )"
  			if [ ${pdfull:0:1} = + ]; then	pdfulle="\e[38;5;046m+\e[0m";else pdfulle="\e[38;5;160m-\e[0m";fi
  			if [ ${pdfull:1:1} = 0 ]; then	pdfulle=$pdfulle" ";else pdfulle=$pdfulle${pdfull:1:1};fi
  			if [ "${pdfull:1:2}" = "00" ]; then	pdfulle=$pdfulle" ";else pdfulle=$pdfulle${pdfull:2:1};fi
  		pdfulle=$pdfulle${pdfull:3:1}
      eval "/home/pi/bitcoindesktoys/show_digitsmove.py $lastreading $usdreading $change" &
      if [[ "$hasunicornhat" -ge "0" ]] && [[ "$usdreading" -ge "10" ]]; then
        eval "/home/pi/bitcoindesktoys/write_history.py $usdreading"
        eval "sudo /home/pi/bitcoindesktoys/unicorn_bars_calculate.py 1"
        eval "touch /home/pi/trigger.foo"
        sleep 10
        eval "sudo /home/pi/bitcoindesktoys/unicorn_bars_calculate.py"
        eval "touch /home/pi/trigger.foo"
      else
        sleep 10
      fi
      echo -en "\$$usdreading($pdfulle) ["
      sleep 30
    fi
  fi
  lastreading=$usdreading
  sleep 1
  while [[ "$(( $(date +%s) % 5 ))" -ne "0" ]];do sleep 0.5;done
done
read -n1 -r -p "Press space to continue..." key
