# ТаксиБер v1.1
Телеграмм-бот, API, сайт, QIWI API, Nominatim и другие сервисы. В данном документе все об установке сервиса на сервер.

## Настройка сервера
Сервер: Ubuntu 20.04

Гайд по базовой настройке Ubuntu-сервера: https://github.com/vasilbekk/ubuntu-setup-django

## Установка и подключение PostgreSQL


Выполняем команду, далее делаем все по гайду ниже:
```sudo apt-get install gcc python3-dev python3-pip python3-venv python3-wheel -y```

Ссылка на гайд: https://github.com/vasilbekk/django-postgresql

### Установка PostGIS
Ссылка на гайд: https://github.com/vasilbekk/geodjango-ubuntu

### Заполнение переменных виртуального окружения
Теперь в корневой директории Django-проекта (core) создаем файл .env и записываем туда данные:
Переменная  | Назначение
------------- | -------------
`DATABASE_NAME`  | Название базы данных PostgreSQL
`DATABASE_USER` | Пользователь базы данных
`DATABASE_PASSWORD` | Пароль
`DATABASE_HOST` | Адрес БД, если на вашей машине, то 127.0.0.1
`DATABASE_PORT` | Порт, обычно 5432
`SECRET_KEY` | Секретный ключ Django
`TELEGRAM_BOT_WEBHOOK_URL` | Базовый URL вебхука Телеграмм-бота
`_TELEGRAM_BOT_SECRET_KEY` | Секретный ключ, который установлен в ТГ-боте
`BASE_URL` | URL, который будет добавлен ко всем статическим и медиа файлам в API. Пример: `http://127.0.0.1:8000`

### Выполняем миграции
```
$ python manage.py makemigrations cabinet dispatcher referral
$ python manage.py migrate
```

## Подключение Телеграмм-бота
Создаем `.env` файл в директории `telegram_bot/` и вставляем туда следующие переменные виртуального окружения:
Переменная  | Назначение
------------- | -------------
`WEBHOOK_SECRET_KEY`  | Секретный ключ для веб-хука свободной формы, указывается в `_TELEGRAM_BOT_SECRET_KEY` настройках ядра
`CORE_TOKEN` | API-Token пользователя для авторизации в ядре. Создаётся: `User.create_token()`
`ADMINS` | Список `chat_id` администраторов в Телеграмме, им будет отправляться уведомления о запуске бота и об остановке
`BOT_TOKEN` | Токен бота в Телеграмм от @BotFather
`ip` | IP-Адрес сервера, на котором находится бот, для веб-хуков
`port` | Порт, на котором вебхук бота будет присылать запрос
`QIWI_TOKEN` | API-Token QIWI-кошелька
`QIWI_PHONE_NUMBER` | Телефонный номер аккаунта, на котором создан `QIWI_TOKEN`
`WEBHOOK_HOST` | IP-Адрес сервера, либо URL-адрес, для вебхука

## Redis
Устанавливаем Redis:
```
sudo apt-get install redis-server
```

Отключаем автозапуск, чтобы не запускался
```
$ sudo systemctl disable redis-server
$ sudo systemctl stop redis-server
```

Создаём файл конфигурации на основе сэмпла
```
$ cp /home/www/taxiber/telegram_bot/data/redis.conf.sample /home/www/taxiber/telegram_bot/data/redis.conf
```

Заполняем конфигурационные данные `redis.conf`
```
...
logfile <logfile_path>
...
dir <work_dir_path>
...
```

Запускаем Redis
```
$ redis-server /home/www/taxiber/telegram_bot/data/redis.conf
```


