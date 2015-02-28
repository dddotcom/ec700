import subprocess

#verification salt
ver_salt = "Uj_y6L*-mhc@77d"
#decryption salt
dec_salt = "FnF4Imd5cQ_z!bF"
#generate a new salt if you want one 
cmd = "cat /dev/urandom | tr -dc '0-9a-zA-Z!@$%^&*_+-' | head -c 15"
new_salt, err = subprocess.Popen(cmd, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
new_salt = new_salt.rstrip('\n')

print "new_salt = " + new_salt

#need a map of command decriptors -> unix commands 
system_info = dict({
	"node name":"uname -n",
	"code name":"lsb_release -cs",
	"language":"echo $LANG"
})

#ask user for these inputs

#generate the keys and output to a file 
