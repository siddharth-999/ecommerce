# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# DATABASE CONNECTION
DATABASES = \
    {
        'default':
            {'ENGINE': 'django.db.backends.postgresql_psycopg2',
             'NAME': 'abc',  # database name
             'USER': 'xyz',  # username
             'PASSWORD': '123456789',  # password
             'HOST': 'localhost',  # host
             'PORT': '5432'  # port number
             }
    }

