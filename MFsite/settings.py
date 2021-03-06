import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = 'sxc%w_&nf^!-7z_k!7@fv47tt7-2mv&8j0wv#kj$&h32=drhmc'
STRIPE_API_KEY_PUBLISHABLE = os.environ['STRIPE_API_KEY_PUBLISHABLE']
STRIPE_API_KEY_SECRET = os.environ['STRIPE_API_KEY_SECRET']

DEBUG = False

ALLOWED_HOSTS = ['masterfaster.herokuapp.com', '127.0.0.1', '.masterfaster.com',]
SECURE_SSL_HOST = 'masterfaster.herokuapp.com'
SECURE_SSL_REDIRECT = True
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
# STATIC_URL = os.path.join(BASE_DIR, 'staticfiles/')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'masterfaster/static'),
    os.path.join(BASE_DIR, 'blog/static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#added for authentication redirect (login)
LOGIN_URL = "masterfaster:login"
LOGIN_REDIRECT_URL = 'masterfaster:home'
LOGOUT_REDIRECT_URL = 'masterfaster:home'

#for custom User Model
AUTH_USER_MODEL = 'masterfaster.User'


# Application definition

INSTALLED_APPS = [
    'masterfaster.apps.MasterfasterConfig',
    'blog.apps.BlogConfig',
    'sales.apps.SalesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#ensure only secure cookies sent
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True

CSRF_COOKIE_HTTPONLY=True
CSRF_FAILURE_VIEW ='masterfaster.views.csrf_failure'

# =======================
# Added Session variables
# =======================
#NOTE: look at clearsessions command to clear sessiondb of sessions not being used

#ensures new login everytime open new browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_COOKIE_AGE --> if set above to Fals, then determine how long cookies last in browser

ROOT_URLCONF = 'MFsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MFsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'MFdb',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'PST8PDT'

USE_I18N = True

USE_L10N = True

USE_TZ = True

##EMAIL SETUP
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'maxjschridde@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_PORT = 587
