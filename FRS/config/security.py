from FRS.config._cfg import ConfigValue, is_type

from django.utils.crypto import get_random_string
import os

# Import secret key or generate new secret key
try:
    import secret_key as sk
except ImportError:
    # Generate Secret Key the same way django-admin's startproject does
    SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    with open(os.path.join(SETTINGS_DIR, 'secret_key.py'), 'w') as f:
        f.write("SECRET_KEY = \"%s\"" % (get_random_string(50, SECRET_KEY_CHARS)))
    import secret_key as sk
    
SECRET_KEY = ConfigValue(sk.SECRET_KEY, condition=is_type(str))          # type: ConfigValue[str]
