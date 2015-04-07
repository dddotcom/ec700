# EC700-Delta2
Project on Oauth Vulnerabilities

This fingerprints whether or not a list of sites are vulnerable to App Impersonation Attacks

There are 2 php files
oauth_clean_parser.php which only outputs the main url it parsed and the results of the fingerprinting
There are 3 possible outcomes 
1. Secure
2. Vulnerable
3. Javascript

-- we assume that Javascript is also vulnerable

oauth_parser.php returns the same results but with details of what the button/link used to assess whether or not the app is vulnerable

Both these files take an html file (in this case delta.html) that has a list of urls in the format <a href="url" ></a>
