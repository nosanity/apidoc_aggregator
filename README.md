## Установка

    Используется python >= 3.5
    pip install -r requirements.txt
    Создать файл с настройками settings/local_settings.py 
    или указать export APIDOC_SETTINGS_PATH=settings_os.docker.py
    и указать в переменных среды нужные настройки
    ./manage.py migrate
    ./manage.py collectstatic --noinput
