#!/bin/bash
function generate_host_id {
	HOSTID=$(/usr/bin/hostid)
	KERNELVERS=$(uname -mrs)
	LANG=$(set | egrep '^(LANG=)')
	LANGUAGE=$(set | egrep '^(LANGUAGE)')
	hostid=$HOSTID$KERNELVERS$LANG$LANGUAGE
	#hostid=$LANGUAGE
	#echo $hostid
}

function generate_key {
	salt="Uj_y6L*-mhc@77d"
	generate_host_id
	#hostid=$(generate_host_id)
	echo "hostid =" $hostid 
	#echo $hostid | wc -c

	#iterative hashing with salt
	key=$(echo -n $(echo -n $salt$hostid | md5sum|awk '{print $1}'))
	echo 1st hash = $key

	#start time for calculating performance
	START=$(date +%s.%N)

	#hash $1 times
	for ((i=2;i<=$1;i++)); 
	do
		key=$(echo -n $(echo -n $key | md5sum|awk '{print $1}'))
	done

	echo $1th hash = $key

	END=$(date +%s.%N)
	echo time elapsed = $(echo $END - $START | bc)s
}

function encrypt {
	if [ -e $DECRYPT_FILENAME ]
	then
		rm *.gpg
	fi
	gpg --batch --passphrase $key -c  $ENCRYPT_FILENAME
}

function decrypt {
	gpg --passphrase $key -d $DECRYPT_FILENAME
}

GPG_AGENT_INFO=""
DECRYPT_FILENAME="hello.c.gpg"
ENCRYPT_FILENAME="hello.c"
SALT="Uj_y6L*-mhc@77d"
#SECOND_SALT="Z5iO6Gk+XJMd^7#"
#VERIFICATION_HASH=""

echo -n "Enter number of times to hash iteratively and press [ENTER]: "
read numHashes
echo "Generating key from host information..."
generate_key $numHashes
#echo SALT=$SALT
#echo hostid passed into python=$hostid
#echo $hostid | wc -c
#output=$(python hash.py "$SALT" "$hostid" "$numHashes")
#echo python output = $output
echo -n "Enter whether you would like to encrypt or decrypt and press [ENTER]: "
read choice
$choice


