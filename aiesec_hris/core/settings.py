"""
Django settings for aiesechr project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
if DEPLOYED:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'aiesechr',
            'USER': 'aiesechr_user',
            'PASSWORD': 'aa212f73',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if DEPLOYED:
    STATIC_ROOT = os.path.join(BASE_DIR, '/usr/share/nginx/html/aiesechr')
    MEDIA_ROOT = os.path.join(BASE_DIR, '/usr/share/nginx/html/aiesechr_media')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOGIN_URL = '/auth/login/'

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=core',
    '--cover-html'
]

COMMENTS_ALLOW_LIKES = False

if not DEPLOYED:
    PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher', ]

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'dreidev_info'
EMAIL_HOST_PASSWORD = 'pass'
DEFAULT_FROM_EMAIL = 'no-reply@dreidev.com'
ADMIN_EMAIL = 'contact@dreidev.com'
