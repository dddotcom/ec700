# an example of a simple web service that is not vulnerable to csrf
# because it implements state based on a value stored in a user's session.

import hmac

from random import getrandbits

from credentials import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET

from flask import Flask, redirect, url_for, session, request
from flask_oauth import OAuth

SECRET_KEY = 'development key'
DEBUG = True

HMAC_KEY = "%x" % getrandbits(128)

mac = hmac.new(HMAC_KEY)

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/v2.2/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


@app.route('/')
def index():
    nonce = "%x" % getrandbits(128)
    session['nonce'] = nonce

    return redirect(url_for('login'))


@app.route('/login')
def login():
   
    mac = hmac.new(HMAC_KEY, session['nonce'])
    state = mac.hexdigest()

    facebook.request_token_params['state'] = state

    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    # Verify the state parameter 
    givenstate = request.args['state']
    nonce = session['nonce']
 
    print "nonce = ", nonce
 
    mac = hmac.new(HMAC_KEY, nonce)
    truestate = mac.hexdigest()

    print "given state: ", givenstate
    print "true state: ", truestate
 
    if truestate != givenstate:
	return 'Access denied: reason="CSRF detected"'

    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s foobar=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'), session['foobar'])

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

if __name__ == '__main__':
    app.run()
