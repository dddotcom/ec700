#!/bin/bash
function generate_host_id {
	HOSTID=$(/usr/bin/hostid)
	KERNELVERS=$(uname -mrs)
	LANGUAGE=$(set | egrep '^(LANG|LC_)')
	local hostid=$HOSTID$KERNELVERS$LANGUAGE
	echo "$hostid"
}

function generate_key {
	salt="Uj_y6L*-mhc@77d"
	hostid=$(generate_host_id)

	#iterative hashing with salt
	key=$(echo -n $(echo -n $salt$hostid | md5sum|awk '{print $1}'))
	echo 1st hash = $key

	#start time for calculating performance
	START=$(date +%s.%N)

	#hash $1 times
	for i in {2..$1}
	do
		key=$(echo -n $(echo -n $key | md5sum|awk '{print $1}'))
		#echo $key
	done

	echo $1th hash = $key

	END=$(date +%s.%N)
	echo time elapsed = $(echo $END - $START | bc)s
}

GPG_AGENT_INFO=""
FILENAME="hello.c"

generate_key 100
#gpg --batch --passphrase $key -c  $FILENAME
