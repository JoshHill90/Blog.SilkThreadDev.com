from decouple import config

class SETTINGS_KEYS:

    djky = config('DJANGO_KEY')
    urne = config('USER_NAME')
    pawd = config('PASSWORD_KEY')
    dbstt = config('DEGUB_STATE', bool)
