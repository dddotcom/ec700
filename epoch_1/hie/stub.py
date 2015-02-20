import datetime
import hashlib
import sys
import subprocess
import os

def main():
	debug = False
	
	#generate host id
	p = subprocess.Popen(["uname", "-n"], stdout=subprocess.PIPE)
	nodename, err = p.communicate()
	nodename = nodename.rstrip('\n')

	p = subprocess.Popen(["lsb_release", "-cs"], stdout=subprocess.PIPE)
	codename, err = p.communicate()
	codename = codename.rstrip('\n')

	my_env=os.environ
	lang = my_env["LANG"]

	hostid = nodename+codename+lang
	salt = "Uj_y6L*-mhc@77d"
	looptimes=10000

	#generate hash
	m = hashlib.md5()
	m.update(salt+hostid)
	tempHash=m.hexdigest()
	if debug:
		firstHash = tempHash

	#hash x times
	start = datetime.datetime.now()
	for x in range(2,looptimes):
		m = hashlib.md5()
		m.update(tempHash)
		tempHash = m.hexdigest()
	duration = datetime.datetime.now() - start

	#print debug statements
	if debug:
		print "salt= '" + salt + "'"
		print "hostid = '" + hostid + "'"
		print "salt+hostid= '" + salt+hostid + "'"
		print "1st hash = '" + firstHash + "'"
		print "10,000th hash = '" + tempHash + "'"
		print "time elapsed = " + str(duration.microseconds/float(1000)) + "ms"

	return tempHash

print main()
