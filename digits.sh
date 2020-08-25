#!/bin/bash
# shellcheck disable=SC2004
eval 'ulimit -S -s 16384' #to help prevent segfault errors when running show_digitsmove
change=$((-1))
hasunicornhat=$(cat /home/pi/config.json | jq '.invert_unicornhat')
echo -e "Watching BTC price movements..."
while : ;do
  usdraw=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
  if echo "$usdraw" | grep -q '{"usd":'  ;then            #data scrape was successful
    usdreading=$(echo "$usdraw" |jq -r '.bitcoin.usd')
    if [ -z "$usdreading" ] || [[ "$usdreading" = "null" ]] || [[ "$usdreading" = "0" ]];then usdreading=$lastreading;fi #in case of timeout
    usdreading=$(printf '%04.0f' "$usdreading")
  else
    usdreading=$lastreading; echo -en "x"; sleep 30;      #data scrape unsuccessful
  fi
  timer=$(( $(date +%_S) + 1 ))
  if ( ( [[ "$timer" -le "55" ]] || [[ "$evernew" -eq "0" ]] ) && ( [[ "$usdreading" = "$LASTREPORTED" ]] || [[ "$usdreading" = "$SecLASTREPORTED" ]] ) ) || ( [[ "$timer" -le "55" ]] && [[ ${#LASTREPORTED} > 1 ]] );then    #price hasnt changed
    if [[ "$usdreading" = "$LASTREPORTED" ]];then         #same value detected
      LASTSAME=$(date +%X)
      echo -en "."
    elif [[ "$usdreading" = "$SecLASTREPORTED" ]];then    #older value detected
      echo -en "p"
    else                                                  #new value detected
      echo -en "n"
      if [[ "$evernew" -eq "0" ]];then
        FOUND=$(date +%s)
        evernew=$((1))
        NEWVALUE=$usdreading
      fi
    fi
  else                                                    #time to report a change in price
    if [[ "$evernew" -eq "0" ]];then FOUND=$(date +%s);else usdreading=$NEWVALUE;evernew=$((0));fi
    if [[ "$usdreading" > "$LASTREPORTED" ]];then
      changeup=$(($change+1))
      change=$(( $changeup > 10 ? 10 : $changeup ))
    else
      changeup=$(($change-1))
      change=$(( $changeup < -10 ? -10 : $changeup ))
    fi
    while [[ "$(( $(date +%_S) + 1 ))" -ne "60" ]] && [[ ${#SecLASTREPORTED} > 1 ]];do sleep 0.05;done #sync multiple units
    if [[ "${#LASTREPORTED}" = "0" ]];then LASTREPORTED=$usdreading  #make first row behave properly
  else echo -e "$(( $FOUND - $START )) seconds] ($FOUND)";fi
    START=$(date +%s)
    eval "/home/pi/bitcoindesktoys/show_digitsmove.py $LASTREPORTED $usdreading $change" &
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
    echo -en "\$$usdreading $(printf '%+03d' $change) $(printf '%+04d' $(( $usdreading - $LASTREPORTED )) )\$ ["
    SecLASTREPORTED=$LASTREPORTED
    LASTREPORTED=$usdreading
  fi
  lastreading=$usdreading
  sleep 1
  while [[ "$(( $(date +%s) % 5 ))" -ne "0" ]];do sleep 0.5;done
done
read -n1 -r -p "Press space to continue..." key
