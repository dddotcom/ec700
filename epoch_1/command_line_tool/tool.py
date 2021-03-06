import subprocess
import hashlib
import binascii
from collections import OrderedDict
import fileinput
import shutil
import sys

keyFile = "key.cpp"
keyTemplate = "keyTemplate.cpp"
hostid_components = ""
debug = False
dk_verify = ""
dk_payload = ""
hostid = ""
verify_salt = "Uj_y6L*-mhc@77d"
payload_salt = "FnF4Imd5cQ_z!bF"
system_info = OrderedDict({
	"Node name":"uname -n",
	"Code name":"lsb_release -cs",
	"Language":"echo $LANG",
	"OS":"uname -o",
	"Public IP":"dig myip.opendns.com @resolver1.opendns.com +short", 
	"Firefox Version":"firefox -v"
})

def get_new_salt():
	#generate a new salt if you want one 
	cmd = "cat /dev/urandom | tr -dc '0-9a-zA-Z!@$%^&*_+-' | head -c 15"
	new_salt, err = subprocess.Popen(cmd, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	new_salt = new_salt.rstrip('\n')
	print "new_salt = " + new_salt


def generate_key():
	global hostid
	global dk_verify
	global dk_payload

	#ask user for these inputs
	if debug:
		hostid = "Ubuntu" + "Trusty" + "en_US.UTF-8"
	else:
		for desc in system_info:
			info = raw_input("Enter " + desc + ": ")
			hostid = hostid + info

	dk_verify = hashlib.pbkdf2_hmac('sha256', hostid, verify_salt, 10000)
	dk_payload = hashlib.pbkdf2_hmac('sha256', hostid, payload_salt, 10000)
	
	dk_verify = binascii.hexlify(dk_verify)
	dk_payload = binascii.hexlify(dk_payload)

	if debug:
		print "hostid = " + hostid
		print "dk_verify = " + dk_verify
		print "dk_payload = " + dk_payload

def output_to_file():
	#generate the keys and output to a file 
	f = open("key.txt", "w")
	f.write("hostid = '" + hostid + "'\n")
	f.write("verify_salt = '" + verify_salt + "'\n")
	f.write("payload_salt = '" + payload_salt + "'\n")
	f.write("dk_verify = '" + dk_verify + "'\n")
	f.write("dk_payload = '" + dk_payload + "'\n")
	f.close()

def create_cpp():
	replaceThis = 'std::string cmdListPy = "";'
	replaceWith = 'std::string cmdListPy = "' + hostid_components + '";'
	
	replaceVerSalt = 'static const char verSalt [] = "";'
	replaceWithVerSalt = 'static const char verSalt [] = "'+ verify_salt +'";'

	replacePayloadSalt = 'static const char decryptSalt [] = "";'
	replaceWithPayloadSalt = 'static const char decryptSalt [] = "'+ payload_salt +'";'

	#create copy of file
	shutil.copy(keyTemplate, keyFile)
	#replace string with my cmds
	for line in fileinput.input(newFile, inplace=True):
		sys.stdout.write(line.replace(replaceThis, replaceWith))
	for line in fileinput.input(newFile, inplace=True):
		sys.stdout.write(line.replace(replaceVerSalt, replaceWithVerSalt))
	for line in fileinput.input(newFile, inplace=True):
		sys.stdout.write(line.replace(replacePayloadSalt, replaceWithPayloadSalt))


#get_new_salt()
#generate_key()
#output_to_file()
create_cpp()


