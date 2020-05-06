#!/bin/bash
# shellcheck disable=SC2004
SPEEDMONITOR=false
DISPLAYDIGITS=false
CHATPRICE=false
maxbarlen=$(cat /home/pi/columnwidth.txt)
if [ ${#maxbarlen} -eq 0 ]; then
	maxbarlen=$((100))
fi
nodeip="127.0.0.1"
chatthreshhold=$((490))
#if [ "$CHATPRICE" = true ]; then /home/ben/go/bin/keybase chat send fucres2 ":roller_coaster: BTC annoucement bot starting up - reporting on any change in price per block greater than \$$chatthreshhold USD";fi
echo  "Catching up to Newest Block..."
while [ -z "$tblok" ] || [[ $tblok = "null" ]] ||  [ -z "$oldmempool" ] || [[ "$oldmempool" = "null" ]] ; do    #|| [[ "$oldmempool" = "0" ]]
	logstatus=$(tail /home/pi/bitcoin/debug.log -n 1|grep progress | cut -f 5,10 -d ' ')
	if [ "$logstatus" != "" ]; then echo "$logstatus";fi
	tblok=$(curl -s --user bongos:goobers --data-binary '{"method": "getblockchaininfo", "params": [] }' http://$nodeip:8332/ | jq '.result.blocks')
	if [ "$SPEEDMONITOR" = true ]; then eval "/home/pi/bitcoindesktoys/setto.py 0";fi
	if [ "$DISPLAYDIGITS" = true ]; then eval "/home/pi/bitcoindesktoys/show_message.py Load" ;fi
	sleep 1
	if [ "$SPEEDMONITOR" = true ]; then eval "/home/pi/bitcoindesktoys/setto.py 3";fi
	sleep 1
	if [ "$SPEEDMONITOR" = true ]; then eval "/home/pi/bitcoindesktoys/setto.py 6";fi
	sleep 1
	oldmempool=$(curl -s --user bongos:goobers --data-binary '{"method": "getmempoolinfo", "params": [] }' http://$nodeip:8332/ | jq '.result.size')
done
nmempool=$(( 1 + $oldmempool ))
mempool=$(( 1 + $oldmempool ))
lastprice=$(( 0 ))
mychar="-";myblank=" ";
while : ;do
  START=$(date +%s)
  oldblok=$tblok
#------------------------------------------------------------------------------
  while [[ "$tblok" = "$oldblok" ]]; do
    oldmempool=$mempool
    mempool=$(curl -s --user bongos:goobers --data-binary '{"method": "getmempoolinfo", "params": [] }' http://$nodeip:8332/ | jq '.result.size')
    while [ -z "$mempool" ] || [[ "$mempool" = "null" ]];do sleep 2; mempool=$(curl -s --user bongos:goobers --data-binary '{"method": "getmempoolinfo", "params": [] }' http://$nodeip:8332/ | jq '.result.size');done #in case of timeout
    RUNTIME=$(( $(date +%s) - $START ))
    case "$((RUNTIME/60%60/10))$((RUNTIME/60%10))" in
     (0[0-2])      cola="\e[38;5;070m";colb="\e[38;5;070m";;
     (0[3-7])      cola="\e[38;5;070m";colb="\e[38;5;229m";;
     (1[2-9])      cola="\e[38;5;229m";colb="\e[38;5;094m";;
     ([2-9][0-9])  cola="\e[38;5;088m";colb="\e[38;5;088m";;
     ( *	)        cola="\e[38;5;229m";colb="\e[38;5;094m";;
    esac
    if [ "$RUNTIME" -ge 3600 ]; then  cola="\e[38;5;088m";colb="\e[38;5;088m";fi #when over an hour keep red
    out="\033[1K\r\e[?25l$(( $tblok + 1 )) \e[38;5;229m$(printf "$cola%01d$colb%01d\e[38;5;229m:%02d" $((RUNTIME/60%100/10)) $((RUNTIME/60%10)) $((RUNTIME%60)))\e[0m $(printf "%05d" "$mempool") "
    nscale=$(( (($mempool/10000)+1)*(10000/$maxbarlen) ))
    if [ "$nscale" != "$scale" ];then
      scale=$nscale
      oldbarlen=$(( $nmempool / $scale ))
    fi
    currbarlen=$(( $mempool / $scale ))
    scalevel=$(( ($mempool/10000)+1 ))
    if [ "$currbarlen" -lt "$oldbarlen" ]; then oldbarlen=$currbarlen;fi
    for (( c=1; c<=$(( $oldbarlen )); c++ )); do
      if   [[ "$scalevel" = "1" ]] || [ "$c" -lt "$((1*$maxbarlen/$scalevel))" ];then
        mychar="-";myblank=" ";       if [[ "$scalevel" -gt "1" ]];then mychar="—";myblank='.';fi
      elif [[ "$scalevel" = "2" ]] || [ "$c" -lt "$((2*$maxbarlen/$scalevel))" ]; then
        mychar="=";myblank='.'
      elif [[ "$scalevel" = "3" ]] || [ "$c" -lt "$((3*$maxbarlen/$scalevel))" ]; then
        mychar="≡";                   if [[ "$scalevel" -gt "4" ]];then myblank='…';fi
      elif [[ "$scalevel" = "4" ]] || [ "$c" -lt "$((4*$maxbarlen/$scalevel))" ]; then
        mychar="‡"
      elif [[ "$scalevel" = "5" ]] || [ "$c" -lt "$((5*$maxbarlen/$scalevel))" ]; then
        mychar="5"
      elif [[ "$scalevel" = "6" ]] || [ "$c" -lt "$((6*$maxbarlen/$scalevel))" ]; then
        mychar="6"
      elif [[ "$scalevel" = "7" ]] || [ "$c" -lt "$((7*$maxbarlen/$scalevel))" ]; then
        mychar="7"
      elif [[ "$scalevel" = "8" ]] || [ "$c" -lt "$((8*$maxbarlen/$scalevel))" ]; then
        mychar="8"
      elif [[ "$scalevel" = "9" ]] || [ "$c" -lt "$((9*$maxbarlen/$scalevel))" ]; then
        mychar="9"
      else
        mychar="z";myblank='…'
      fi
      out+=$mychar
    done
		if [[ $(($maxbarlen/$scalevel)) -lt "10" ]];then scalevel=$(($maxbarlen/10));fi
    for (( c=1; c<=$(( $currbarlen - $oldbarlen )); c++ )); do out+="#";done
    for (( c=1; c<=$(( $maxbarlen - $currbarlen )); c++ )); do
      if [ "$(( ($c + $currbarlen) % ($maxbarlen / 10 / $scalevel ) ))" == "0" ];then out+="+";else out+=${myblank}; fi;  done
    if [[ "$(( $RUNTIME%5 ))" -eq "0" ]] || [[ "$lastprice" = "0" ]];then
			echo -en "O"
			usdprice=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
			if echo "$usdprice" | grep -q "bitcoin"  ;then
				usdprice=$(echo "$usdprice" |jq -r '.bitcoin.usd')
				if [ -z "$usdprice" ] || [[ "$usdprice" = "null" ]] || [[ "$usdprice" = "0" ]];then usdprice=$lastprice;fi #in case of timeout
				if [[ "$lastprice" = "0" ]]; then lastprice=$usdprice; fi #set historical value for first row
				echo -en "@"
			else
				usdprice=$lastprice
			fi
			if [ "$DISPLAYDIGITS" = true ]; then eval "/home/pi/bitcoindesktoys/show_message.py $(printf '%04.0f' $usdprice)" ;fi
    fi
		pdfull="$(printf '%+06.2f' "$(echo $usdprice - $lastprice | bc )" )"
		echo -en "${out} \$$(printf "%07.2f" $usdprice)($pdfull)  $(( ( (10 * ($mempool-$nmempool) /(RUNTIME+1) )+5)/10 ))/s"
    sleep .5s
		echo -en "."
		tblok=$(curl -s --user bongos:goobers --data-binary '{"method":"getblockchaininfo","params":[]}' http://$nodeip:8332/ | jq '.result.blocks')
    if [[ -z "$tblok" || $tblok = "null" ]]; then tblok=$oldblok;fi #in case of timeout
		speedval=$(( ( (10 * ($mempool-$nmempool) /(RUNTIME+1) )+5)/10 ))
    if [[ "$oldval" != "$speedval" && "$SPEEDMONITOR" = true ]];then eval "/home/pi/bitcoindesktoys/setto.py $speedval";oldval=$speedval;fi
		echo -en "o"
		#if [ -e "/home/ben/newbolt.txt" ];then eval "/home/ben/cycle2count.py 6";rm /home/ben/newbolt.txt;fi
  done
#------------------------------------------------------------------------------
  nmempool=$(curl -s --user bongos:goobers --data-binary '{"method": "getmempoolinfo", "params": [] }' http://$nodeip:8332/ | jq '.result.size')
  while [ -z "$nmempool" ] || [[ "$nmempool" = "null" ]] || [[ "$nmempool" = "0" ]];do sleep 2; nmempool=$(curl -s --user bongos:goobers --data-binary '{"method": "getmempoolinfo", "params": [] }' http://$nodeip:8332/ | jq '.result.size');  done #in case of timeout
  scale=$(( (($oldmempool/10000)+1)*(10000/$maxbarlen) ))
	bakedin=$(( $oldmempool - $nmempool ))
  currbarlen=$(( $oldmempool / $scale ))
  oldbarlen=$(( $nmempool / $scale ))
  if [ "$currbarlen" -lt "$oldbarlen" ]; then oldbarlen=$currbarlen;fi
  echo -en "\033[1K\r\e[?25l${out:0:$(( ${#out} + $oldbarlen - $maxbarlen ))}"
  case "${bakedin}" in
    ([5-9][0-9][0-9][0-9])  echo -en "\e[38;5;163m";;
    (4[5-9][0-9][0-9])      echo -en "\e[38;5;076m";;
    (4[0-4][0-9][0-9])      echo -en "\e[38;5;114m";;
    (3[5-9][0-9][0-9])      echo -en "\e[38;5;070m";;
    (3[0-4][0-9][0-9])      echo -en "\e[38;5;064m";;
    (2[5-9][0-9][0-9])      echo -en "\e[38;5;106m";;
    (2[0-4][0-9][0-9])      echo -en "\e[38;5;100m";;
    (1[5-9][0-9][0-9])      echo -en "\e[38;5;058m";;
    (1[0-4][0-9][0-9])      echo -en "\e[38;5;094m";;
     ([5-9][0-9][0-9])      echo -en "\e[38;5;088m";;
    ( *	)                   echo -en "\e[38;5;052m";;
  esac
  for (( c=1; c<=$(( $currbarlen - $oldbarlen )); c++ )); do echo -n "O";done
  echo -en "\e[0m"
  for (( c=1; c<=$(( $maxbarlen - $currbarlen )); c++ )); do
    if [ "$(( ($c + $currbarlen) % ( $maxbarlen / 10 / $scalevel ) ))" == "0" ];then echo -n "+";else echo -n "${myblank}"; fi;  done
  pdfull="$(printf '%+06.2f' "$(echo $usdprice - $lastprice | bc )" )"
	echo -e  "\e[0m \$$(printf "%07.2f" $usdprice)($pdfull) [$(printf "%04d" ${bakedin})tx] $(date '+%H:%M')"
	if [ "$CHATPRICE" = true ]; then
		if [ "$(printf '%.0f' "$pdfull")" -gt "$chatthreshhold" ]; then
    	echo "price  up  to $usdprice from $lastprice -- $pdfull "
    	/home/ben/go/bin/keybase chat send fucres2 ":roller_coaster: :chart_with_upwards_trend: price up \$$pdfull to $usdprice from $lastprice"
  	fi
  	if [ "$(printf '%.0f' "$pdfull")" -lt "$(( 0 - $chatthreshhold ))" ] && [ "$usdprice"  -gt "0" ]; then
    	echo "price down to $usdprice from $lastprice -- $pdfull "
    	/home/ben/go/bin/keybase chat send fucres2 ":roller_coaster: :chart_with_downwards_trend: price down \$$pdfull to $usdprice from $lastprice"
  	fi
	fi
  lastprice=$usdprice
  if [ -f "/home/pi/bitcoindesktoys/cuckoo.wav" ]; then eval "aplay -q /home/pi/bitcoindesktoys/cuckoo.wav" ; fi
	#if [ -f "/home/pi/bitcoindesktoys/playtone.py" ]; then eval "/home/pi/bitcoindesktoys/playtone.py" ; fi
done
