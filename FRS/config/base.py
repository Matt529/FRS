from typing import Set
from FRS.config._cfg import ConfigValue, is_type, contained_type, join
from funcy.types import is_set

import os

BASE_DIR = os.path.abspath(__file__ + '/../../../')
DEBUG = True

ALLOWED_HOSTS = {
    '*'
}

BASE_DIR = ConfigValue(BASE_DIR, condition=is_type(str))                                    # type: ConfigValue[str]
DEBUG = ConfigValue(DEBUG, condition=is_type(bool))                                         # type: ConfigValue[bool]
ALLOWED_HOSTS = ConfigValue(ALLOWED_HOSTS, condition=join(is_set, contained_type(str)))     # type: ConfigValue[Set[str]]

LOGGING_DIR = ConfigValue(os.path.join(BASE_DIR.value, 'logs'), condition=is_type(str))     # type: ConfigValue[str]
