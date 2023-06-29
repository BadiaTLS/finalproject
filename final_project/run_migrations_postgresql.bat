@echo off
REM activate virtual environment
call %~dp0tavenv\Scripts\activate.bat
set PROMPT=(tavenv) $P$G

REM set PostgreSQL password
set PGPASSWORD=my_db@123

REM clear local PostgreSQL database
psql -U hero -d my_db -c "DROP DATABASE my_db;"

REM recreate database and import users from CSV file
psql -U hero -c "CREATE DATABASE my_db;"

REM run Django migrations and create superuser
python final_project\manage.py makemigrations
python final_project\manage.py migrate

set DJANGO_SUPERUSER_USERNAME=admin
set DJANGO_SUPERUSER_EMAIL=admin@example.com
set DJANGO_SUPERUSER_PASSWORD=admin
python manage.py createsuperuser --noinput

set DJANGO_SUPERUSER_USERNAME=sassas
set DJANGO_SUPERUSER_EMAIL=sas@example.com
set DJANGO_SUPERUSER_PASSWORD=sassas
python manage.py createsuperuser --noinput

set DJANGO_SUPERUSER_USERNAME=dininghall
set DJANGO_SUPERUSER_EMAIL=dininghall@example.com
set DJANGO_SUPERUSER_PASSWORD=dininghall
python manage.py createsuperuser --noinput

REM run Django server
python manage.py runserver

REM deactivate virtual environment
call tavenv\Scripts\deactivate.bat
pause
