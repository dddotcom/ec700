import datetime
import hashlib
import sys

def main():
	if len(sys.argv) != 4:
		print "This program outputs the iterative md5 hash of a string made up of a 16 byte salt concatenated with a hostid string. \nNot enough arguments. \nRun this program with the following inputs:"
		print "\tpython hash.py [salt] [hostid] [times to iteratively hash]"
		return None

	salt = sys.argv[1]
	print "salt= " + salt
	hostid=sys.argv[2]
	print "hostid = " + hostid
	looptimes=int(sys.argv[3])+1

	#generate hash
	m = hashlib.md5()
	m.update(salt+hostid)
	tempHash=m.hexdigest()
	print "1st hash = " + tempHash

	#hash x times
	start = datetime.datetime.now()
	for x in range(2,looptimes):
		m = hashlib.md5()
		m.update(tempHash)
		tempHash = m.hexdigest()
		#print tempHash
	print sys.argv[3] +"th hash = " + tempHash
	duration = datetime.datetime.now() - start
	print "time elapsed = " + str(duration.microseconds/float(1000)) + "ms"
	return tempHash
main()
