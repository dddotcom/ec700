RECONNECT
=========

Our implmentation of Egor Homakov's Reconnect Attack. The only part that's missing
is the service's oauth url to do single sign on with Facebook. Since we don't want 
people to flat out copy this and use it against services, we don't include possible
URLs here. Instead, the url should be embedded after the hash inside the phishing link 
that an attacker sends to a victim. An example link will be presented in our report.

In order to run this code, you will need to set up a Facebook Canvas App and use 
the 307me.php file in this directory as the URL. Fortunately, we already set this
up, so you can just use our Facebook app url given in oauth.js.
