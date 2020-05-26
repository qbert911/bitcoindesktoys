#!/bin/bash
# shellcheck disable=SC2004
lastreading=$((0))
change=$((-1))
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
    echo -en "."
  else
    if [[ "$usdreading" > "$lastreading" ]];then
      changeup=$(($change+1))
      change=$(( $changeup > 10 ? 10 : $changeup ))
    else
      changeup=$(($change-1))
      change=$(( $changeup < -10 ? -10 : $changeup ))
    fi
    if [[ "$lastreading" = "0" ]];then lastreading=$usdreading;START=$(($START+10));fi  #make first row behave properly
    #eval "/home/pi/bitcoindesktoys/show_digitsmove.py $lastreading $usdreading $change"
    eval "/home/pi/bitcoindesktoys/write_history.py $usdreading"
    echo -en "\n\$$usdreading $(printf '%+03d' $change) $(printf '%+04d' $(( $usdreading - $lastreading )) )\$ change  $(( $(date +%s) - $START )) seconds"
    START=$(date +%s)
  fi
  lastreading=$usdreading
  sleep 10
done
