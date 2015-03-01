#include <iostream>
#include <cstring>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>

/****************************************************** Globals **************************************************************/
static const char verSalt [] = "P05@E+hdMBGV+JqA"; // Value will be passed by python tool
static const char decryptSalt [] = "W4LZ!e-QkxQKg#Z*"; // Value will be passed by python tool
static const int bufLen = 60; // Length of buffers that will store command outputs

// Commands
const char osCmd[] = "uname -o";
const char codeNameCmd[] = "lsb_release -cs";
const char langCmd[] = "echo $LANG";
const char firefoxVerCmd[] = "firefox -v";
const char extIpCmd[] = "dig myip.opendns.com @resolver1.opendns.com +short";
		
/****************************************************** Function(s) **********************************************************/
std::string getSysInfo(const char *cmd) {
	std::string result = "";
	char buf[bufLen];
	FILE *fp = popen(cmd, "r");
	if (fp == NULL) {
		printf("Error: could not fetch external IP from key.cpp file.\n");
	}

	while (!feof(fp)) {
		if (fgets(buf, bufLen, fp) != NULL) {
			result += buf;
		}
	}

	fclose(fp);

	return result.c_str(); // Return the C-style string
}


/****************************************************** Main *****************************************************************/
// Call the chosen functions, concatenate the outputs, and return the resulting string (i.e. the "password")

int main()
{
	//std::string cmdListPy = "extIpCmd;firefoxVerCmd;langCmd;"; // List of commands passed by the python tool
	std::string cmdListPy = "extIpCmd;";
	std::string delimiter = ";";
	int pos = 0;
	std::string token;
	std::string hostId = "";
	const char * hostIdFinal;

	// Parse the list of commands passed by the Python tool and map the tokens to the commands needed to execute 
	while ((pos = cmdListPy.find(delimiter)) != std::string::npos) {
		token = cmdListPy.substr(0, pos); // Parse out a command from the string passed by the Python tool
		//std::cout << token << std::endl; // DEBUGGING

		if (token == "osCmd") {
			hostId += getSysInfo(osCmd);
		}

		if (token == "codeNameCmd") {
			hostId += getSysInfo(codeNameCmd);
		}
    
		if (token == "langCmd") {
			hostId += getSysInfo(langCmd);
		}

		if (token == "firefoxVerCmd") {
			hostId += getSysInfo(firefoxVerCmd);
		}

		if (token == "extIpCmd") {
			hostId += getSysInfo(extIpCmd);
		}

		cmdListPy.erase(0, pos + delimiter.length());
	}

	// Remove the newlines
	hostId.erase(std::remove(hostId.begin(), hostId.end(), '\n'), hostId.end());

	// Print out values
	std::cout << "Host ID: " << hostId << std::endl; // DEBUGGING
	std::cout << "Verification salt: " << verSalt << std::endl; // DEBUGGING
	std::cout << "Decryption salt: " << decryptSalt << std::endl; // DEBUGGING
	
	// Convert host ID to C-style string
	hostIdFinal = hostId.c_str(); 
	
	return 0;
}

 
/*********************************************** Old Code (Reference only) ***************************************************/
/*

// Get OS of targeted system
std::string getOs() {
  const char cmd[]= "uname -o";
  std::string result = "";
  unsigned char buf[bufLen];
  FILE *fp = popen(cmd, "r");
  if (fp == NULL) {
    printf("Error: could not fetch OS from key.cpp file.\n");
  }

  while (!feof(fp)) {
    if (fgets(buf, bufLen, fp) != NULL) {
      result += buf;
    }
  }

  fclose(fp);

  return result.c_str(); // Return the C-style string
}


// Get code name of targeted system ---> Linux command $ lsb_release -cs
std::string getCodeName()
{
  std::string codeName = "";
  const char codeNameCmd[]= "lsb_release -cs";
  char buf[bufLen];
  FILE *fp = popen(codeNameCmd, "r");
  if (fp == NULL) {
    printf("Error: could not fetch Firefox version from key.cpp file.\n");
  }

  while (!feof(fp)) {
    if (fgets(buf, bufLen, fp) != NULL) {
      codeName += buf;
    }
  }

  fclose(fp);

  return codeName.c_str(); // Return the C-style string
}


// Get LANG environment variable of targeted system
std::string getLang() 
{
  const char langCmd[]= "echo $LANG";
  std::string lang = "";
  char buf[bufLen];
  FILE *fp = popen(langCmd, "r");
  if (fp == NULL) {
    printf("Error: could not fetch LANG variable from key.cpp file.\n");
  }

  while (!feof(fp)) {
    if (fgets(buf, bufLen, fp) != NULL) {
      lang += buf;
    }
  }

  fclose(fp);

  return lang.c_str(); // Return the C-style string
}


// Get Firefox Browser version ---> Linux command firefox -v (add regex to get into format "Firefox/31.0")
std::string getFirefoxVer()
{
  const char cmd[]= "firefox -v";
  std::string output = "";
  char buf[bufLen];
  FILE *fp = popen(cmd, "r");
  if (fp == NULL) {
    printf("Error: could not fetch Firefox version from key.cpp file.\n");
  }

  while (!feof(fp)) {
    if (fgets(buf, bufLen, fp) != NULL) {
      output += buf;
    }
  }

  fclose(fp);

  return output.c_str(); // Return the C-style string
}


// Get external IP of targeted system
std::string getExtIp() { 
  const char cmd[]= "dig myip.opendns.com @resolver1.opendns.com +short";
  std::string result = "";
  unsigned char buf[bufLen];
  FILE *fp = popen(cmd, "r");
  if (fp == NULL) {
    printf("Error: could not fetch external IP from key.cpp file.\n");
  }

  while (!feof(fp)) {
    if (fgets(buf, bufLen, fp) != NULL) {
      result += buf;
    }
  }

  fclose(fp);

  return result.c_str(); // Return the C-style string
}

  std::string test = "";
  test = getSysInfo(osCmd);
  std::cout << "Test: " << test << std::endl;

  // Uncomment to test "getExtIp" function
  std::string extIp = "";
  extIp = getExtIp();
  std::cout << "External IP: " << extIp << std::endl;
 

  // Uncomment to test "getOs" function
  std::string os = "";
  os = getOs();
  std::cout << "OS: " << os << std::endl;
  

  // Uncomment to test "getLang" function
  std::string lang = "";
  lang = getLang();
  std::cout << "LANG environment variable: " << lang << std::endl;


  // Uncomment to test "getFirefoxVer" function
  std::string ver = "";
  ver = getFirefoxVer();
  std::cout << "Firefox version: " << ver << std::endl;s
  

  // Uncomment to test "getCodeName" function
  std::string codeName = "";
  ver = getCodeName();
  std::cout << "Code name: " << codeName << std::endl;
*/
