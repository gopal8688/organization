from base.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^9hbucdy*&rg#$q+ea7_@5+n+$^9^h9-7ydv!gz7&io--d3&hm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'authsafe_customer', #database name
        'USER': 'root', #username
        'PASSWORD': 'Sl7@1234',
        #'PASSWORD': 'toor',
        'HOST': 'localhost', #'95.216.170.200',
        'PORT': '3306',
    },
    # 'mongoc': {
    #     'ENGINE': 'djongo',
    #     'NAME': 'ml_logs',
    # }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = "/var/www/html/customer/base/static/"
STATIC_URL = '/cstatic/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'base/static')              #os.path.join(BASE_DIR, 'login/static')
# ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
MEDIA_URL = '/media/'

SITE_URL = 'http://localhost/customer/'

LOGIN_URL = SITE_URL