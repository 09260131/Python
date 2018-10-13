#!/bin/bash
case $1 in 
	CLOSE_WAIT|ESTABLISHED|FIN_WAIT2|Foreign|TIME_WAIT)
		/bin/netstat -tnp | awk '{print $6}' | sort -n | uniq -c | grep $1 | awk '{print $1}'
		;;
	SVNUP)
		/bin/cat /tmp/errlog.svnup | wc -l
		;;	
	connected_clients|used_memory_human)
	    echo info | redis-cli -a 91Mwbyd! -x | grep $1 | awk -F: '{print $2}'	
		;;	
	access_log)
        TIME=`/usr/bin/python /etc/zabbix/scripts/nginx_log.py`
        cat /var/log/nginx/access.log | grep "$TIME" | wc -l
		;;
    nfsmt)
       df -h | grep '10.0.146.7:/var/lib/nows' > /dev/null
       RETVAL1=$?
       df -h | grep '10.0.146.7:/d/tools' > /dev/null
       RETVAL2=$?
       RETVAL=$(($RETVAL1+$RETVAL2))
       echo $RETVAL
       ;;
    is_rsync)
    	SEC=`date "+%s"`
    	SEC_REM=`cat /var/www/html/plugins/rsync.test1`
    	MIN=$(($SEC - $SEC_REM))
        echo $MIN
    	;;
    time_update)
         state_file=/tmp/check_ntp_status.log
         [ -f $state_file ] || /bin/touch $state_file
         [ -s $state_file ] && echo 1 || echo 0
         ;;
	*)
esac
