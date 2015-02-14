import datetime
import hashlib
import sys

#salt = "Uj_y6L*-mhc@77d" #hardcoded 
salt = sys.argv[2]
print "salt= " + salt
hostid1=str(sys.argv[3])
print "hostid1 = " + hostid1
hostid="007f0101Linux 3.13.0-32-generic x86_64LANG=en_US.UTF-8 LANGUAGE=en_US"
print "hostid = " + hostid
print hostid1==hostid
print str(hostid1)==str(hostid)

#generate hash
m = hashlib.md5()
m.update(salt+hostid1)
tempHash=m.hexdigest()
print "1st hash1 = " + tempHash

#generate hash
m = hashlib.md5()
m.update(salt+hostid)
tempHash=m.hexdigest()
print "1st hash = " + tempHash

#looptimes=int(sys.argv[1])+1
#hash 10000 times
#start = datetime.datetime.now()
#for x in range(2,looptimes):
#	m = hashlib.md5()
#	m.update(tempHash)
#	tempHash = m.hexdigest()
	#print tempHash
#print sys.argv[1]+"th hash = " + tempHash
#duration = datetime.datetime.now() - start
#print "time elapsed = " + str(duration.microseconds/float(1000)) + "ms"
