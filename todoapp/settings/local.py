# local.py is default django settings file
from .base import *

DEBUG = True

ALLOWED_HOSTS += ["127.0.0.1", '*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db',
    }
}

REDIS = (os.environ.get('REDIS_HOST', ''), int(os.environ.get('REDIS_PORT', 0)))
CHANNEL_LAYERS = {
    'default' : {
        'BACKEND' : 'channels_redis.core.RedisChannelLayer',
        'CONFIG' : {
            'hosts' : [REDIS]
        },
    }
}

LIMITED_TODO_COUNT=10**3
