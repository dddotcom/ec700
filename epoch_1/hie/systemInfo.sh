#!/bin/bash

#--------------collect info----------------------
HOSTID=$(/usr/bin/hostid)
KERNELVERS=$(uname -mrs)
IPADDR=$(ifconfig -a | grep "inet addr")
INSTALLEDSOFTWARE=$(dpkg --list)
LANGUAGE=$(set | egrep '^(LANG|LC_)')

#--------------print out info--------------------
#echo HOSTID:  $HOSTID
#echo KERNELVERS: $KERNELVERS
#echo LANGUAGE: $LANGUAGE

#-------------generate key----------------------
#use this to generate random 16bytes from /dev/urandom
random="$(cat /dev/urandom | tr -dc '0-9a-zA-Z!@#$%^&*_+-' | head -c 15)"
echo random = $random
echo $random | wc -c

salt="Uj_y6L*-mhc@77d"
echo salt = $salt
echo $salt | $wc -c
salt2="Z5iO6Gk+XJMd^7#"
echo salt2 = $salt2
echo $salt2 | wc -c
hostid=$salt$HOSTID$KERNELVERS$LANGUAGE
echo hostid = $hostid

#iterative hashing with salt
hash=$(echo -n $(echo -n $hostid | md5sum|awk '{print $1}'))
echo 1st hash = $hash

#start time for calculating performance
START=$(date +%s.%N)

#hash 1000 times
for i in {2..100}
do
	hash=$(echo -n $(echo -n $hash | md5sum|awk '{print $1}'))
	#echo $hash
done

echo 1000th hash = $hash

END=$(date +%s.%N)
echo time elapsed = $(echo $END - $START | bc)s
