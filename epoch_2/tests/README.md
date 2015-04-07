OAuth 2 Attacks
===============

This is a simple flask app that allows a user to log in using their
Facebook account. The app redirects to Facebook for authorization, then
Facebook sends the user back to the app and some Facebook info is displayed.
You need to have a Facebook app and store its App ID and App Secret inside 
a file called

    credentials_local.py

with the following format

    settings = {
        "FACEBOOK_APP_ID": "appid",
        "FACEBOOK_APP_SECRET": "appsecret",
    }

You can ask Will for the appid or app secret. Alternatively, you can
set up your own Facebook App if you wish. You should be able to modify
this example to work with other IPs as well.

We have set up a Facebook App that does not whitelist any specific
redirect URI. This means you can redirect to any path on a domain, 
which is a vulnerability.

To run the example, you need to edit your /etc/hosts file to point
oauthattacks.com (a fake domain that we gave to Facebook) to the
localhost. Add the following to /etc/hosts

    127.0.0.1 oauthattacks.com

You will need to install the following software to run this code:

    - python 2.7.*
    - flask (python module)
    - flask_oauth (python module)

Then, run csrf.py and try to log in using Facebook.

    python csrf.py

Open a web browser and go to 

    oauthattacks.com:5000
