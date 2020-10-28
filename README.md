# Сайт-аукцион с элитной недвижимостью

## Установка

1. Клонируйте репозиторий, создайте виртуальное окружение
2. Установите зависимости `pip install -r requirements.txt`
3. Создайте файл config.py и создайте в нем переменные:
  ```
  basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

REMEMBER_COOKIE_DURATION = timedelta(days=10)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'Впишите Ваш секретный ключ шифрования'
  ```