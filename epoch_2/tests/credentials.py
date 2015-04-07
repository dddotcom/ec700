try:
    from credentials_local import settings as settings_local
except:
    settings_local = {}

FACEBOOK_APP_ID = settings_local.get('FACEBOOK_APP_ID', '')
FACEBOOK_APP_SECRET = settings_local.get('FACEBOOK_APP_SECRET', '')
