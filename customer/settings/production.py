from customer.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^9hbucdy*&rg#$q+ea7_@5+n+$^9^h9-7ydv!gz7&io--d3&hm'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['client.authsafe.ai']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'authsafe_customer', #database name
        'USER': 'authsafe', #username
        'PASSWORD': 'dRQs5YGRh]+fuL8>',
        'HOST': '10.10.10.6', #'95.216.170.200',
        'PORT': '3306',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/logs/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = "/home/stroth/customer/customer/static/"
STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'customer/static')              #os.path.join(BASE_DIR, 'login/static')
# ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
MEDIA_URL = '/media/'

SITE_URL = 'https://client.authsafe.ai/'

LOGIN_URL = SITE_URL