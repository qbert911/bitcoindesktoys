#!/bin/bash
# shellcheck disable=SC2004
lastreading=$((0))
change=$((-1))
hasunicornhat=$(cat /home/pi/config.json | jq '.invert_unicornhat')
echo -e "Watching BTC price movements..."
while : ;do
  usdraw=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
  if echo "$usdraw" | grep -q "bitcoin"  ;then  #data scrape was successful
    usdreading=$(echo "$usdraw" |jq -r '.bitcoin.usd')
    usdreading=$(printf '%04.0f' "$usdreading")
    if [ -z "$usdreading" ] || [[ "$usdreading" = "null" ]] || [[ "$usdreading" = "0" ]];then usdreading=$lastreading;fi #in case of timeout
  else  usdreading=$lastreading;  echo -en "x";sleep 20; fi #data scrape unsuccessful

  if [[ "$usdreading" = "$lastreading" ]];then    #price hasnt changed
    if [[ "$dotcounter" -gt "2" ]];then
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
    if [[ "$lastreading" = "0" ]];then lastreading=$usdreading  #make first row behave properly
    else echo -e "$(( $(date +%s) - $START )) seconds]";fi

    eval "/home/pi/bitcoindesktoys/write_history.py $usdreading"
    eval "/home/pi/bitcoindesktoys/show_digitsmove.py $lastreading $usdreading $change" &
    if [[ "$hasunicornhat" -ge "0" ]]; then
      eval "sudo /home/pi/bitcoindesktoys/unicorn_bars.py 1"
      sleep 10
      ZOOM=$(cat /home/pi/config.json | jq '.zoom_level')
      eval "sudo /home/pi/bitcoindesktoys/unicorn_bars.py $ZOOM"
    else
      sleep 10
    fi
    echo -en "\$$usdreading $(printf '%+03d' $change) $(printf '%+04d' $(( $usdreading - $lastreading )) )\$ ["
    START=$(date +%s)
    dotcounter=$((0))
  fi
  lastreading=$usdreading
  dotcounter=$(($dotcounter+1))
  sleep 3
done
