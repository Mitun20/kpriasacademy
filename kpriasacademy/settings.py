"""
Django settings for kpriasacademy project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8)t-2^k*6@inpv_pf7xo8111y2od3im0w7(n6k)i!r639tm_+)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['portal.kpriasacademy.in','www.portal.kpriasacademy.in']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'account',
    'mcq_test',
    'tseries',   
    'subject',
    'ckeditor',
    'course',
    'daily_mcq',
    'scholarship',
    'import_export',
    'assignment',
    'mains_test_series',
    'rest_framework',
   
   
    
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kpriasacademy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

             'libraries':{            
            'enrollment_tags'      : 'templatetags.enrollment_tags',
            'test_due_date_tags'   : 'templatetags.test_due_date_tags',            
            'check_attempt_tags'   : 'templatetags.check_attempt_tags',            
            'check_answer_tags'    : 'templatetags.check_answer_tags',
            'login_form_tags'      : 'templatetags.login_form_tags',
            'highest_and_lowest_mark_tags': 'templatetags.highest_and_lowest_mark_tags',
            'sort_apps'            : 'templatetags.sort_apps',
            'batch_filter'            : 'templatetags.batch_filter',
            'check_course_enrolment_batch':'templatetags.check_course_enrolment_batch',

            }
            
        },
    },
]

WSGI_APPLICATION = 'kpriasacademy.wsgi.application'
X_FRAME_OPTIONS = 'ALLOWALL'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


APP_ORDER = [
    'account',
    'subject',
    'course',
    'tseries',
    'mains_test_series',    
    'mains_course',
    'daily_mcq',
    'scholarship',
    'mcq_test', 
]



DATABASES = {

   'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'kpr_ias',
        'USER': 'root',
        'PASSWORD': 'PNR4erp!!!',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = 'profile_photo/uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'height': 100,
        'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'width': 800,
       
        'toolbar_Custom': [
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike','Superscript', 'Subscript',  '-',]},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},           
            {'name': 'links', 'items': ['Link']},
             {'name': 'insert',
             'items': ['Image', 'Smiley']},
      
            {'name': 'clipboard', 'items': ['Undo', 'Redo']},
             {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList',  'Blockquote', 
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', 
                       ]},
            {'name': 'math', 'items': ['Mathjax', ]},
        ],
        
        'toolbar': 'Custom',
        'mathJaxLib': '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML',
        'extraPlugins': ','.join(['mathjax',]),
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


BASE_DIR1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATIC_URL = '/static/'

STATICFILES_DIRS = ( os.path.join('static'), )

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media' 

AUTH_USER_MODEL = 'account.User'


LOGIN_REDIRECT_URL = 'home'


LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL ='login'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'z2k5-jfth.accessdomain.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'webmaster@kpriasacademy.in' 
EMAIL_HOST_PASSWORD = 'SvhQk0{8k?}'
