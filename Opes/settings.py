from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG =bool(int(os.environ.get('DEBUG',0)))
SECRET_KEY = os.environ.get('SECRET_KEY')



ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "django.contrib.sitemaps",
    'Populus.apps.PopulusConfig',
    'crispy_forms',
    'Porta.apps.PortaConfig',
    'Participes.apps.ParticipesConfig',
    'Topic.apps.TopicConfig',
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'mptt',
    'FollowUser.apps.FollowuserConfig',
    'Vote.apps.VoteConfig',
    'Daily.apps.DailyConfig',
    'Brand.apps.BrandConfig',
    'Profil.apps.ProfilConfig',   
    'notifications',
    'social_django', 
    'django_json_ld',
     "django.contrib.postgres",
     "storages",
    'corsheaders',
     
]
SITE_ID = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',    

    
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOWED_ORIGINS = [ 'http://localhost:3030',]
CORS_ALLOWED_ORIGIN_REGEXES = ['http://localhost:3030',]


SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = "same-origin"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 
X_FRAME_OPTIONS = 'SAMEORIGIN'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

ROOT_URLCONF = 'Opes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
              
            ],               
            
        },
    },
]

WSGI_APPLICATION = 'Opes.wsgi.application'

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': os.environ.get('POSTGRES_DB'),

        'USER': os.environ.get('POSTGRES_USER'),

        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),

        'HOST': 'pgdb',

        'PORT': 5432,
        'URL':os.environ.get('DATABASE_URL')

    }

}
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_ROOT = os.path.join(BASE_DIR,"staticfiles")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,"static"),
)



CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = 'user:login'
AWS_S3_GZIP = True
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY =os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

AWS_S3_REGION_NAME = 'eu-central-1'
AWS_S3_FILE_OVERWRITE=False
LOCATION ='media'
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = 'Opes.storages.MediaStore'

CKEDITOR_FILE_STORAGE='Opes.storages.MediaStore'
DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}
CACHE_LOCATION="redis://redis:6379"
REDIS_DB_FSM=0
REDIS_DB_JOBSTORE=1
CACHES = {
 "redis": {
 "BACKEND": "redis_cache.RedisCache",
 "LOCATION": CACHE_LOCATION,
 "TIMEOUT": 60, 
 "KEY_PREFIX": "Opes",
  'OPTIONS': {
            'DB': 1,           
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            'PICKLE_VERSION': -1,
            "IGNORE_EXCEPTIONS": True,
        },
 },
}
CACHES["default"] = CACHES["redis"]
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

DEFAULT_AUTO_FIELD ="django.db.models.BigAutoField"




EMAIL_HOST = 'smtppro.zoho.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = 465
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
SERVER_EMAIL = EMAIL_HOST_USER
ADMINS = [(os.environ.get('ADMIN'), os.environ.get('DJANGO_SUPERUSER_EMAIL'))]

AUTHENTICATION_BACKENDS = [
     
    'django.contrib.auth.backends.ModelBackend',
     'Populus.authentication.EmailAuthBackend',
    'social_core.backends.google.GoogleOAuth2',
   
   
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

)


CACHED_STORAGE = False
TAGGIT_CASE_INSENSITIVE = True

LOGIN_URL = '/login/'

CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_REQUIRE_STAFF=False



CKEDITOR_RESTRICT_BY_USER = True

CKEDITOR_BROWSE_SHOW_DIRS = True

CKEDITOR_JQUERY_URL = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"




CKEDITOR_FORCE_JPEG_COMPRESSION = True

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
     
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  
            {'name': 'yourcustomtools', 'items': [
              
                'Preview',
                'Maximize',
                'CodeSnippet',
               

            ]},
            
        ],
       
        
        'toolbar': 'YourCustomToolbarConfig',  
        'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 291,
        'width': '100%',
        'filebrowserWindowHeight': 725,
        'filebrowserWindowWidth': 940,
        'toolbarCanCollapse': True,
        'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', 
          
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'codesnippet'
           
        ]),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
        'root': {
            'handlers': ['console', 'log_file'],
            'level': 'INFO',
           
        },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(module)s] %(message)s',
       
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,           
            
        },
        'log_file':{
            'level':'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename' :'djangoproject.log',
            'formatter' :'verbose'
        } 
    },
    'loggers': {
        'django': {
            'handlers': ['console','mail_admins'],
            'propagate': True,
            'level':'INFO'
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}
