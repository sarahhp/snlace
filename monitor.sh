

echo 'PID   S   CPU   MEM   CMD' 
while sleep 15m; do date '+%F %X'; ps --noheaders -o pid,s,%cpu,%mem,cmd; done

#topp() (
#  $* &>/dev/null &
 # pid="$!"
  #trap ':' INT
  #echo 'CPU  MEM'
  #while sleep 15m; do ps --no-headers -o '%cpu,%mem' -p "$pid" ; done
  #kill "$pid"
#)
#topp ./commands.sh
