#!/bin/bash
# shellcheck disable=SC2004
lastreading=$((0))
change=$((-1))
dotcounter=$((0))
START=$(date +%s)
echo -en "Watching BTC price movements..."
while : ;do
  usdraw=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
  if echo "$usdraw" | grep -q "bitcoin"  ;then  #data scrape was successful
    usdreading=$(echo "$usdraw" |jq -r '.bitcoin.usd')
    usdreading=$(printf '%04.0f' "$usdreading")
    if [ -z "$usdreading" ] || [[ "$usdreading" = "null" ]] || [[ "$usdreading" = "0" ]];then usdreading=$lastreading;fi #in case of timeout
  else  usdreading=$lastreading;  fi #data scrape unsuccessful

  if [[ "$usdreading" = "$lastreading" ]];then
    if [[ "$dotcounter" = "3" ]];then
      echo -en "."
      dotcounter=$((0))
    fi
  else
    if [[ "$usdreading" > "$lastreading" ]];then
      changeup=$(($change+1))
      change=$(( $changeup > 10 ? 10 : $changeup ))
    else
      changeup=$(($change-1))
      change=$(( $changeup < -10 ? -10 : $changeup ))
    fi
    if [[ "$lastreading" = "0" ]];then lastreading=$usdreading;START=$(($START+10));fi  #make first row behave properly
    echo -e "$(( $(date +%s) - $START )) seconds"
    eval "/home/pi/bitcoindesktoys/write_history.py $usdreading"
    eval "/home/pi/bitcoindesktoys/show_digitsmove.py $lastreading $usdreading $change" &
    eval "sudo /home/pi/bitcoindesktoys/unicorn_bars.py 1"
    sleep 10
    ZOOM=$(cat /home/pi/config.json | jq '.zoom_level')
    eval "sudo /home/pi/bitcoindesktoys/unicorn_bars.py $ZOOM"
    echo -en "\$$usdreading $(printf '%+03d' $change) $(printf '%+04d' $(( $usdreading - $lastreading )) )\$ change"
    START=$(date +%s)
  fi
  lastreading=$usdreading
  sleep 3;dotcounter=$(( $dotcounter + 1))
done
