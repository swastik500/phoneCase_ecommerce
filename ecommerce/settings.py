import os
from pathlib import Path
from dotenv import load_dotenv

# Load env variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    # ...
    # Local Apps
    'core',
    'accounts',
    'catalog',
    'cart',
    'orders',
    'payments',
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

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom Cart Context Processor (we will build this later)
                'cart.context_processors.cart', 
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Database (Default SQLite for Dev)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata' # Set to India
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout Redirects
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# # Razorpay Config
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

# # PayPal Settings
# PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
# PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
# PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'sandbox')


# EMAIL CONFIGURATION

# OPTION A: For Development (Prints email to Command Prompt/Terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# OPTION B: For Real Gmail (Use this when you are ready to go live)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') # Your Gmail address
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # App Password (not login password)

# The email address that sends the emails
DEFAULT_FROM_EMAIL = 'CaseHaven Store <no-reply@casehaven.com>'
# The Shop Owner's email (Where you receive alerts)
ADMIN_EMAIL = 'admin@yourstore.com'
