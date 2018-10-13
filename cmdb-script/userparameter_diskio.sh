#!/bin/bash
source /etc/profile

function rrqmps(){
    DISK=$1
    VAULE=`iostat -x -d -m 1 2 | grep "$DISK" | tail -1 | awk '{print $2}'`
    echo $VAULE
}
function wrqmps(){
    DISK=$1
    VALUE=`iostat -x -d -m 1 2 | grep "$DISK" | tail -1 | awk '{print $3}'`
    echo $VALUE
}
function rps(){
    DISK=$1
    VAULE=`iostat -x -d -m 1 2 | grep "$DISK" | tail -1 | awk '{print $4}'`
    echo $VAULE
}
function wps(){
    DISK=$1
    VAULE=`iostat -x -d -m  1 2 | grep "$DISK" | tail -1 | awk '{print $5}'`
    echo $VAULE
}
function rspeed(){
    DISK=$1
    VAULE=`iostat -x -d -m 1 2 | grep "$DISK" | tail -1 | awk '{print $6}'`
    echo $VAULE
}
function wspeed(){
    DISK=$1
    VAULE=`iostat -x -d -m  1 2 | grep "$DISK" | tail -1 | awk '{print $7}'`
    echo $VAULE
}
function await(){
    DISK=$1
    VAULE=`iostat -x -d -m 1 2 | grep "$DISK" | tail -1 | awk '{print $10}'`
    echo $VAULE
}
function svctm(){
    DISK=$1
    VAULE=`iostat -x -d -m 1 2 | grep "$DISK" | tail -1 | awk '{print $11}'`
    echo $VAULE
}
function util(){
    DISK=$1
    VAULE=`iostat -x -d -m 1 2 | grep "$DISK" | tail -1 | awk '{print $12}'`
    echo $VAULE
}

case $2 in
        rrqmps)
                rrqmps $1
        ;;
        wrqmps)
                wrqmps $1
        ;;
        rps)
                rps $1
        ;;
        wps)
                wps $1
        ;;
        rspeed)
                rspeed $1
        ;;
        wspeed)
                wspeed $1
        ;;
        await)
                await $1
        ;;
        svctm)
                svctm $1
        ;;
        util)
                util $1
        ;;
        *)
esac















