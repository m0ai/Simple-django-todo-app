from .base import *

DEBUG = False

ALLOWED_HOSTS += ["127.0.0.1", '*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DJANGO_DB_NAME', ''),
        'USER': os.environ.get('DJANGO_DB_USERNAME', ''),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DB_HOST', ''),
        'PORT': os.environ.get('DJANGO_DB_PORT', ''),
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

LIMITED_TODO_COUNT=10**5
