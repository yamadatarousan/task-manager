INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',  # アプリを追加
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'task_manager_db',
        'USER': 'root',  # 必要に応じて変更
        'PASSWORD': '',   # 必要に応じて変更
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

TIME_ZONE = 'Asia/Tokyo'  # 日本時間に設定

SECRET_KEY = 'HB7a6W9hJO2kn3vBKmk_qUnyvYESQTyaSMZrXd7HgUTfihPmHtN9JKPEYFrmK-gSgdA'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # テンプレートディレクトリを指定（必要に応じて追加）
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # セッション管理
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 認証
    'django.contrib.messages.middleware.MessageMiddleware',  # メッセージ
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]