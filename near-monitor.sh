#!/bin/bash
#
# Created by William Guozi
#
NET=$1
while true; do
        #启动一个循环，定时检查进程是否存在
        server=`ps aux | grep near-$NET-monitor | grep -v grep`
        if [ ! "$server" ]; then
            #如果不存在就重新启动
	          nearup $NET
            nohup  python /root/near-$NET-monitor.py >> /root/near-$NET-monitor.log 2>&1 &
            #启动后沉睡10s
            sleep 10
        fi
        #每次循环沉睡60s
        sleep 60
done
