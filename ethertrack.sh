#!/bin/bash
mycurrencyinput=$((5043))
lastsaneout=$((0))
while : ;do

  curl -s https://api.ethplorer.io/getAddressInfo/0x8D82Fef0d77d79e5231AE7BFcFeBA2bAcF127E2B?apiKey=EK-d81D6-5s7p3du-G9q7j -o /home/pi/myethwallet.json
  curl -s https://api.ethplorer.io/getAddressInfo/0x3041cbd36888becc7bbcbc0045e3b1f144466f5f?apiKey=EK-d81D6-5s7p3du-G9q7j -o /home/pi/targetpool.json
  #curl -s https://api.ethplorer.io/getTokenInfo/0x3041cbd36888becc7bbcbc0045e3b1f144466f5f?apiKey=EK-d81D6-5s7p3du-G9q7j -o targettoken.txt

  if cat /home/pi/myethwallet.json |grep -q UNI-V2 ;then            #data scrape was successful
    mytokens=$(cat /home/pi/myethwallet.json | jq '.tokens[]| select(.tokenInfo.address |contains("0x3041cbd36888becc7bbcbc0045e3b1f144466f5f"))|.balance')
    mytokensu=$(cat /home/pi/myethwallet.json | jq '.tokens[]| select(.tokenInfo.address |contains("0x3041cbd36888becc7bbcbc0045e3b1f144466f5f"))|.tokenInfo.lastUpdated')
    totalsupply=$(cat /home/pi/myethwallet.json | jq '.tokens[]| select(.tokenInfo.address |contains("0x3041cbd36888becc7bbcbc0045e3b1f144466f5f"))|.tokenInfo.totalSupply|tonumber')
  else
   echo -en "x"; sleep 20       #data scrape unsuccessful
  fi

  if cat /home/pi/targetpool.json |grep -q USDC ;then            #data scrape was successful
    totalusdc=$(cat /home/pi/targetpool.json | jq '.tokens[0].balance')
    totalusdt=$(cat /home/pi/targetpool.json | jq '.tokens[1].balance')
    totalusdcu=$(cat /home/pi/targetpool.json | jq '.tokens[0].tokenInfo.lastUpdated')
    totalusdtu=$(cat /home/pi/targetpool.json | jq '.tokens[1].tokenInfo.lastUpdated')
  else
   echo -en "y"; sleep 20       #data scrape unsuccessful
  fi

  age1=$(echo $(date +%s) - $mytokensu |bc)
  age2=$(echo $(date +%s) - $totalusdcu |bc)
  age3=$(echo $(date +%s) - $totalusdtu |bc)

  mypercent=$(echo $mytokens / $totalsupply |bc -l)
  myusdt=$(echo $mypercent *$totalusdt/1000000 |bc -l)
  myusdc=$(echo $mypercent *$totalusdc/1000000 |bc -l)

  myout=$(printf "%.2f\n" "$(echo $myusdt + $myusdc | bc -l)")

  pmyusdt=$(printf "%.4f\n" "$(echo $myusdt| bc -l)")
  pmyusdc=$(printf "%.4f\n" "$(echo $myusdc| bc -l)")
  pmypercent=$(printf "%.8f\n" "$(echo $mypercent| bc -l)")

  if  [[ "$lastsaneout" = "$myout" ]] || [[ "$bad_out" = "$myout" ]];then    #price hasnt changed
    dotcounter=$dotcounter+1
    if [[ "$dotcounter" -eq "10" ]];then
      echo -en "\033[9DO          \033[10D"
      dotcounter=$((0))
    else
      echo -en "."
    fi
  else
    dotcounter=$((0))
    thisdiff=$(printf "%.0f\n" "$(echo $lastsaneout *100 - $myout *100 | bc -l)")
    pthisdiff=$(printf "%.2f\n" "$(echo $myout - $lastsaneout | bc -l)")
    if [[ "$thisdiff" -le "-200000" ]];then thisdiff=$((0));pthisdiff="    ";fi
    if [[ "$thisdiff" -le "-25" ]] || [[ "$thisdiff" -gt "0" ]];then
      mycolor="\e[38;5;196m";bad_out=$myout;diffdiff=$lastdiff-$thisdiff;
      if [[ "$thisdiff" -ge "-75" ]] && [[ "$thisdiff" -le "-25" ]] && [[ "$diffdiff" -eq "1" ]] ;then
        mycolor="\e[38;5;168m"
        #        mycolor="\e[38;5;208m";        mycolor="\e[38;5;190m"
      fi
      lastdiff=$thisdiff
    else
      mycolor="\e[38;5;070m";lastsaneout=$myout
      lsmyusdt=$myusdt
      lsmyusdc=$myusdc
    fi
    pthisdiff=$mycolor$pthisdiff"\e[0m"

    #if [[ "$last_totalsupply" = "$totalsupply" ]];then
        #echo -en "\n$(date +%m/%d@%T) $mycolor$myoutd$myout\e[0m            ($pmyusdt $pmyusdc) [ $pthisdiff ] "
    #else
      #if [[ "$last_totalusdc" = "$totalusdc" ]];then
        #echo -en "\n$(date +%m/%d@%T) $mycolor$myoutd$myout\e[0m $pmypercent                       [ $pthisdiff ] "
      #else
        #echo -en "\n$(date +%m/%d@%T) $mycolor$myoutd$myout\e[0m $pmypercent ($pmyusdt $pmyusdc) [ $pthisdiff ] "
      #fi
    #fi
    echo -en "\n$(date +%m/%d@%T) $mycolor$myout\e[0m [ $pthisdiff ] "
    if [[ "$age1" -ge "4800" ]] || [[ "$age2" -ge "2400" ]] || [[ "$age3" -ge "2400" ]];then
        echo -en " [ STALE $age1 $age2 $age3 ] [ $totalsupply $(echo $totalusdt/1000000 |bc) $(echo $totalusdc/1000000 |bc) ] "
    fi
  fi

  if [[ "$(date +%M)" == "00" ]];then
    dotcounter=$((0))
    echo -en "\n$(date +%m/%d@%T) \e[38;5;086m$lastsaneout\e[0m"
    echo $(date +%m,%d,%T),$(printf '%.4f\n' "$(echo $lsmyusdt + $lsmyusdc | bc -l)")>> /home/pi/uniswaplog.csv
    eval sudo /home/pi/share/bitcoindesktoys/ethlogprocess.sh
    echo -en " "
    eval "/home/pi/share/bitcoindesktoys/feth16.sh"
    eval "touch /home/pi/triggerhd.foo"
    sleep 60
  fi
  last_totalsupply=$totalsupply
  last_totalusdc=$totalusdc
  sleep 6
done
