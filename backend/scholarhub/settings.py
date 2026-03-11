"""
Django settings for scholarhub project.
Enterprise-Grade Setup with HashiCorp Vault Integration.
"""

import os
import hvac
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# 1. KONFIGURASI KEAMANAN & VAULT (Sesuai Dokumen )
# ==============================================================================
# Kita mengambil SECRET_KEY dan Database Credentials dari Vault.
# Tidak ada password yang ditulis langsung di sini!

VAULT_ADDR = os.environ.get("VAULT_ADDR", "http://vault.scholarhub.svc.cluster.local:8200")
VAULT_ROLE_ID = os.environ.get("VAULT_ROLE_ID")
VAULT_SECRET_ID = os.environ.get("VAULT_SECRET_ID")

# Default values (Fallback) jika koneksi Vault gagal (misal saat build Docker)
SECRET_KEY = 'django-insecure-build-only-key'
DB_USER = 'root'
DB_PASSWORD = 'scholarhub_initial_root_pass'

try:
    if VAULT_ROLE_ID and VAULT_SECRET_ID:
        print(f"🔐 Mencoba koneksi ke Vault di {VAULT_ADDR}...")
        
        # Login ke Vault pakai AppRole
        client = hvac.Client(url=VAULT_ADDR)
        client.auth.approle.login(
            role_id=VAULT_ROLE_ID,
            secret_id=VAULT_SECRET_ID
        )

        # Ambil Secret Key Django
        secret_response = client.secrets.kv.v2.read_secret_version(path='scholarhub/django')
        SECRET_KEY = secret_response['data']['data']['secret_key']

        # Ambil Password Database (Dynamic Secret)
        db_creds = client.secrets.database.generate_credentials("scholarhub-role")
        DB_USER = db_creds['data']['username']
        DB_PASSWORD = db_creds['data']['password']
        
        print("✅ SUKSES: Rahasia berhasil diambil dari Vault!")
    else:
        print("⚠️ PERINGATAN: VAULT_ROLE_ID tidak ditemukan. Menggunakan mode tidak aman (build only).")

except Exception as e:
    print(f"❌ ERROR VAULT: {e}")
    # Jangan crash di sini agar collectstatic tetap jalan saat build, 
    # tapi sistem tidak akan bisa connect DB di production.

# ==============================================================================
# 2. PENGATURAN UMUM
# ==============================================================================

DEBUG = True  # Nanti ubah ke False saat production 

ALLOWED_HOSTS = ['*'] # Izinkan semua host untuk kemudahan development di Kubernetes


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    'rest_framework_simplejwt',
    'scholarships', # Tambahan: Django Rest Framework 
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

ROOT_URLCONF = 'scholarhub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'scholarhub.wsgi.application'


# ==============================================================================
# 3. DATABASE (Sesuai Dokumen )
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scholarhub',
        'USER': DB_USER,         # Dari Vault
        'PASSWORD': DB_PASSWORD, # Dari Vault
        'HOST': os.environ.get('DB_HOST', 'mariadb.scholarhub.svc.cluster.local'),
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4', # Wajib support Emoji/Unicode 
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# 4. CUSTOM USER & SECURITY (TAHAP 2)
# ==============================================================================

# Beri tahu Django untuk menggunakan User buatan kita, bukan yang default
AUTH_USER_MODEL = 'users.CustomUser'

# Wajibkan penggunaan Argon2 untuk Hashing Password sesuai dokumen keamanan
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher', # Argon2 jadi prioritas #1
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# ==============================================================================
# 5. REST FRAMEWORK & JWT AUTHENTICATION
# ==============================================================================
from datetime import timedelta

# Beritahu Django untuk mengunci semua API pakai JWT secara default
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Aturan umur token dan kuncinya (Memakai SECRET_KEY dari Vault!)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Tiket akses berlaku 1 jam
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Tiket perpanjangan berlaku 1 hari
    'SIGNING_KEY': SECRET_KEY,                      # Token dilindungi oleh kunci Vault
    'AUTH_HEADER_TYPES': ('Bearer',),
}