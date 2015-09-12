# Django settings for myproject project.
import os
DEVLOPMENT_MODE = False
MAINTENANCE_MODE = False

MYSQLMODE = False
PGSQLMODE = True
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
                               
if DEVLOPMENT_MODE:
    DEBUG = True
    TEMPLATE_DEBUG = True
    TEMPLATE_STRING_IF_INVALID = 'INVALID VARIABLE'
    CACHE_BACKEND ='locmem:///' 
    CACHE_TIMEOUT = 60*5
    CACHE_PREFIX="Z"
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
else:
    DEBUG = False
    TEMPLATE_DEBUG = False
    TEMPLATE_STRING_IF_INVALID = ''
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    CACHE_BACKEND ='locmem:///' 
    CACHE_TIMEOUT = 60*5
    CACHE_PREFIX="Z"

    
ADMINS = (
     ('Eric Satterwhite', 'webmaster@muskegohitmen.com'),
)
MANAGERS = (
    ('Samantha Radloff', 'samantha@samanthajoyphotography.com'),
)
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'sjphoto'
EMAIL_HOST_PASSWORD = 'da93bfac'
DEFAULT_FROM_EMAIL = 'noreply@samanthajoyphotography.com'
SERVER_EMAIL = 'noreply@samanthajoyphotohraphy.com'

if MYSQLMODE:
    DATABASE_ENGINE = 'mysql'
    DATABASE_USER = 'erics'
    DATABASE_PASSWORD = 'qxm8uavi'

if PGSQLMODE:
    DATABASES = {
        'default':{
            "ENGINE":'django.db.backends.postgresql_psycopg2',
            "NAME":"jshenk",
            "USER":'jshenk',
            "PASSWORD":'PloI098$'
        }
    }


TIME_ZONE = 'America/Chicago'
INTERNAL_IPS = ('127.0.0.1',)
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
#adding a comment
USE_I18N = False
ACCOUNT_ACTIVATION_DAYS = 7
FORCE_LOWERCASE_TAGS = True
COMMENTS_HIDE_REMOVED = True
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
STATIC_DOC_ROOT = 'media/'
MEDIA_ROOT = PROJECT_ROOT + '/media/'
#MEDIA_ROOT = '/home/sjphoto/webapps/nginx/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://127.0.0.1:8000/static_media/'
MEDIA_URL = 'http://media.jennischenk.com/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dn4d@jqg^+%&ww79dihu*0f^s#f!96^*8vyk4ih-=1nhc-+8_k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)
THUMBNAIL_PROCESSORS = (
    # Default processors - sorl thumbnail
    'sorl.thumbnail.processors.colorspace',
    'sorl.thumbnail.processors.autocrop',
    'sorl.thumbnail.processors.scale_and_crop',
    'sorl.thumbnail.processors.filters',
    )


MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'django.middleware.transaction.TransactionMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    "django.middleware.doc.XViewMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

)
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug', # comment out when in production
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)
ROOT_URLCONF = 'sjphoto.urls'
DJAPIAN_DATABASE_PATH = 'djapian_spaces/'
DJAPIAN_STEMMING_LANG = "en"
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT +'/templates',
    '/home/webapps/sjphoto_wsgi/lib/python2.5/debug_toolbar/templates',
)
#AUTHENTICATION_BACKENDS = (
#   'satchmo_store.accounts.email-auth.EmailBackend',
#   'django.contrib.auth.backends.ModelBackend',  
#)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django_extensions',
    'template_utils',
    'debug_toolbar',
    'contact_form',
    'pagination',
    'hotsauce',
    'debug_toolbar',
    'overexposure',
    'maintenancemode',
    'south',
    'tagging',
    'djapian',
    'registration',
    'sorl.thumbnail',
    'imagekit',
    'messages',
    'sjphoto.base',
    'likeables',
)
