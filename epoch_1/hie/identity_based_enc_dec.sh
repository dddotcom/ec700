#!/bin/bash
function generate_host_id {
	HOSTID=$(/usr/bin/hostid)
	KERNELVERS=$(uname -mrs)
	LANG=$(set | egrep '^(LANG=)')
	LANGUAGE=$(set | egrep '^(LANGUAGE)')
	hostid=$HOSTID$KERNELVERS$LANG$LANGUAGE
	#echo $hostid
}

function generate_key {
	salt="Uj_y6L*-mhc@77d"
	generate_host_id
	echo "hostid =" $hostid 

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

#generate key using python script, much faster
function generate_key_python {
	echo -e "\nhost id =$hostid"
	START=$(date +%s.%N)
	key=$(python hash.py "$SALT" "$hostid" "$numHashes" 2>&1)
	END=$(date +%s.%N)
	#echo time elapsed = $(echo $END - $START | bc)s
	echo -e "$1th hash =$key\n"
}

#encrypt hello.c with gpg 
function encrypt {
	if [ -e $DECRYPT_FILENAME ]
	then
		rm *.gpg
	fi
	gpg --batch --passphrase $key -c  $ENCRYPT_FILENAME
}

#decrypt hello.c.gpg with gpg
function decrypt {
	if [ -e $DECRYPT_FILENAME ] 
	then 
		gpg --passphrase $key -d $DECRYPT_FILENAME
	else
		echo "Can't decrypt: $DECRYPT_FILENAME does not exist"
	fi
}

GPG_AGENT_INFO=""
DECRYPT_FILENAME="hello.c.gpg"
ENCRYPT_FILENAME="hello.c"
SALT="Uj_y6L*-mhc@77d"
#SECOND_SALT="Z5iO6Gk+XJMd^7#"
#VERIFICATION_HASH=""

numHashes=""
while [[ ! $numHashes =~ ^[0-9]+$ ]]; do
    echo -n "Enter number of times to hash iteratively and press [ENTER]: "
    read numHashes
done

generate_host_id
echo "Generating key from host information..."
generate_key_python $numHashes

echo -n "Enter whether you would like to encrypt or decrypt and press [ENTER]: "
read choice

while [[ $choice != encrypt && $choice != decrypt ]]; do
	echo "string doesn't match"
	echo -n "Enter whether you would like to encrypt or decrypt and press [ENTER]: "
	read choice

done
$choice





