#!/bin/bash
if [ $# -lt 1 ]; then
	echo "$0 imgfile tapidx memorysize"
	echo "    tapinterface -> default tap0 interface"
	echo "    memorysize -> default 512"
	echo "    vnc display-> default none"
	exit
fi
imgfile=$1
tap="0"
mem="512"
if [ $# -ge 2 ]; then
	tap=$2
fi
if [ $# -ge 3 ]; then
	mem=$3
fi
vnc=''
if [ $# -ge 4 ]; then
	vnc=$4
fi
macaddr[0]="52:54:00:00:00:01"
macaddr[1]="52:54:00:00:00:02"
macaddr[2]="52:54:00:00:00:03"
macaddr[3]="52:54:00:00:00:04"
macaddr[4]="52:54:00:00:00:05"
macaddr[5]="52:54:00:00:00:06"
cmd="kvm -enable-kvm -drive file=$imgfile,if=virtio,cache=writeback -m $mem -vga std -rtc base=localtime,clock=host -smp 1 -display none -net nic,macaddr=${macaddr[$tap]} -net tap,ifname=tap$tap,script=no,downscript=no -balloon virtio -daemonize"
if  [ $vnc ] ; then
	cmd=$cmd" -vnc :$vnc"
fi
echo $cmd
$cmd
