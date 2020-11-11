#!/bin/bash
# shellcheck disable=SC2004
maxbarlen=$(cat /home/pi/config.json | jq '.column_width')
show_speed=$(cat /home/pi/config.json | jq '.show_speed')
if [ ${#maxbarlen} -eq 0 ]; then
	maxbarlen=$((100))
fi
nodeip="127.0.0.1"
echo  "Catching up to Newest Block..."
while [ -z "$tblok" ] || [[ $tblok = "null" ]] || [ -z "$oldmempool" ] || [[ "$oldmempool" = "null" ]] ; do
	logstatus=$(tail /home/pi/bitcoin/debug.log -n 1|grep progress | cut -f 5,10 -d ' ')
	if [ "$logstatus" != "" ]; then echo "$logstatus";fi
	tblok=$(curl -s --user bongos:goobers --data-binary '{"method": "getblockchaininfo", "params": [] }' http://$nodeip:8332/ | jq '.result.blocks')
	sleep 3
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
     (1[2-9])      cola="\e[38;5;229m";colb="\e[38;5;220m";;
     ([2-9][0-9])  cola="\e[38;5;196m";colb="\e[38;5;196m";;
     ( *	)        cola="\e[38;5;229m";colb="\e[38;5;229m";;
    esac
    if [ "$RUNTIME" -ge 3600 ]; then  cola="\e[38;5;196m";colb="\e[38;5;196m";fi #when over an hour keep red
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
        mychar="4"
      elif [[ "$scalevel" = "6" ]] || [ "$c" -lt "$((6*$maxbarlen/$scalevel))" ]; then
        mychar="5"
      elif [[ "$scalevel" = "7" ]] || [ "$c" -lt "$((7*$maxbarlen/$scalevel))" ]; then
        mychar="6"
      elif [[ "$scalevel" = "8" ]] || [ "$c" -lt "$((8*$maxbarlen/$scalevel))" ]; then
        mychar="7"
      elif [[ "$scalevel" = "9" ]] || [ "$c" -lt "$((9*$maxbarlen/$scalevel))" ]; then
        mychar="8"
			elif [[ "$scalevel" = "10" ]] || [ "$c" -lt "$((10*$maxbarlen/$scalevel))" ]; then
        mychar="9"
			elif [[ "$scalevel" = "11" ]] || [ "$c" -lt "$((11*$maxbarlen/$scalevel))" ]; then
        mychar="0"
			elif [[ "$scalevel" = "12" ]] || [ "$c" -lt "$((12*$maxbarlen/$scalevel))" ]; then
        mychar="1"
			elif [[ "$scalevel" = "13" ]] || [ "$c" -lt "$((13*$maxbarlen/$scalevel))" ]; then
        mychar="2"
			elif [[ "$scalevel" = "14" ]] || [ "$c" -lt "$((14*$maxbarlen/$scalevel))" ]; then
        mychar="3"
			elif [[ "$scalevel" = "15" ]] || [ "$c" -lt "$((15*$maxbarlen/$scalevel))" ]; then
        mychar="4"
			elif [[ "$scalevel" = "16" ]] || [ "$c" -lt "$((16*$maxbarlen/$scalevel))" ]; then
        mychar="5"
      else
        mychar="Z";myblank='…'
      fi
      out+=$mychar
    done
		if [[ $(($maxbarlen/$scalevel)) -lt "10" ]];then scalevel=$(($maxbarlen/10));fi
    for (( c=1; c<=$(( $currbarlen - $oldbarlen )); c++ )); do out+="#";done
    for (( c=1; c<=$(( $maxbarlen - $currbarlen )); c++ )); do
      if [ "$(( ($c + $currbarlen) % ($maxbarlen / 10 / $scalevel ) ))" == "0" ];then out+="+";else out+=${myblank}; fi;  done
    if [[ "$(( $RUNTIME%6 ))" -eq "0" ]] || [[ "$lastprice" = "0" ]];then
			echo -en "O"
			usdprice=$(curl -s -X GET "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" -H "accept: application/json")
			if echo "$usdprice" | grep -q '{"usd":'  ;then
				usdprice=$(echo "$usdprice" |jq -r '.bitcoin.usd')
				if [ -z "$usdprice" ] || [[ "$usdprice" = "null" ]] || [[ "$usdprice" = "0" ]];then usdprice=$lastprice;fi #in case of timeout
				if [[ "$lastprice" = "0" ]]; then lastprice=$usdprice; fi #set historical value for first row
				echo -en "@"
			else
				usdprice=$lastprice
			fi
    fi
		pdfull="$(printf '%+04.0f' "$(echo $usdprice - $lastprice | bc )" )"

		if [ ${pdfull:1:3} = "000" ];then pdfulle="      ";else
			if [ ${pdfull:0:1} = + ]; then	pdfulle="(\e[38;5;046m+\e[0m";else pdfulle="(\e[38;5;160m-\e[0m";fi
			if [ ${pdfull:1:1} = 0 ]; then	pdfulle=$pdfulle" ";else pdfulle=$pdfulle${pdfull:1:1};fi
			if [ "${pdfull:1:2}" = "00" ]; then	pdfulle=$pdfulle" ";else pdfulle=$pdfulle${pdfull:2:1};fi
			pdfulle=$pdfulle${pdfull:3:1}")"
		fi
		echo -en "${out} \$$(printf "%04.0f" $usdprice)$pdfulle  $(( ( (10 * ($mempool-$nmempool) /(RUNTIME+1) )+5)/10 ))/s"
    sleep .5s
		echo -en "."
		tblok=$(curl -s --user bongos:goobers --data-binary '{"method":"getblockchaininfo","params":[]}' http://$nodeip:8332/ | jq '.result.blocks')
    if [[ -z "$tblok" || $tblok = "null" ]]; then tblok=$oldblok;fi #in case of timeout
		speedval=$(( ( (10 * ($mempool-$nmempool) /(RUNTIME+1) )+5)/10 ))
    if [[ "$oldval" != "$speedval" ]] && [[ "$show_speed" -eq "1" ]];then
			eval "/home/pi/bitcoindesktoys/piglow_speed.py $speedval"
			eval "/home/pi/bitcoindesktoys/rainbowhat_speed.py $speedval"
			oldval=$speedval
		fi
		echo -en "o"
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
	echo -e  "\e[0m \$$(printf "%04.0f" $usdprice)$pdfulle [$(printf "%04d" ${bakedin})tx] $(date '+%H:%M')"
  lastprice=$usdprice
  if [ "$RUNTIME" -ge 10 ] && [ -f "/home/pi/bitcoindesktoys/cuckoo.wav" ]; then eval "nice -n -11 aplay -q /home/pi/bitcoindesktoys/cuckoo.wav" ; fi
done
