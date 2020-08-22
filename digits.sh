#!/bin/bash
# shellcheck disable=SC2004
#eval 'ulimit -S -s 16384' #to help prevent segfault errors when running show_digitsmove
lastreading=$((0))
change=$((-1))
hasunicornhat=$(cat /home/pi/config.json | jq '.invert_unicornhat')
echo -e "Watching BTC price movements..."
while : ;do
  usdraw=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
  if echo "$usdraw" | grep -q '{"usd":'  ;then  #data scrape was successful
    usdreading=$(echo "$usdraw" |jq -r '.bitcoin.usd')
    if [ -z "$usdreading" ] || [[ "$usdreading" = "null" ]] || [[ "$usdreading" = "0" ]];then usdreading=$lastreading;fi #in case of timeout
    usdreading=$(printf '%04.0f' "$usdreading")
  else  usdreading=$lastreading;  echo -en "x";sleep 30; fi #data scrape unsuccessful

  if [[ "$usdreading" = "$lastreading" ]];then    #price hasnt changed
    if [[ "$dotcounter" -gt "1" ]];then
      echo -en "."
      dotcounter=$((0))
    fi
  else
    FOUND=$(date +%X)
    while [[ "$(( $(date +%_S) % 19 ))" -ne "0" ]];do sleep 0.05;done #sync multiple units
    if [[ "$usdreading" > "$lastreading" ]];then
      changeup=$(($change+1))
      change=$(( $changeup > 10 ? 10 : $changeup ))
    else
      changeup=$(($change-1))
      change=$(( $changeup < -10 ? -10 : $changeup ))
    fi
    if [[ "$lastreading" = "0" ]];then lastreading=$usdreading  #make first row behave properly
    else echo -e "$(( $(date +%s) - $START )) seconds] $FOUND $(date +%X)";fi
    START=$(date +%s)
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
    echo -en "\$$usdreading $(printf '%+03d' $change) $(printf '%+04d' $(( $usdreading - $lastreading )) )\$ ["
    sleep 40
    dotcounter=$((0))
  fi
  lastreading=$usdreading
  dotcounter=$(($dotcounter+1))
  sleep 1
  while [[ "$(( $(date +%s) % 5 ))" -ne "0" ]];do sleep 0.05;done
done
read -n1 -r -p "Press space to continue..." key
