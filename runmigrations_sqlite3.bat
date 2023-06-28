call %~dp0tavenv\Scripts\activate.bat
set PROMPT=(tavenv) $P$G

IF EXIST final_project\db.sqlite3 DEL /F final_project\db.sqlite3

python final_project\manage.py makemigrations
python final_project\manage.py migrate

@echo off
set DJANGO_SUPERUSER_USERNAME=admin
set DJANGO_SUPERUSER_EMAIL=admin@example.com
set DJANGO_SUPERUSER_PASSWORD=admin
python final_project\manage.py createsuperuser --noinput

@echo off
echo from final_project.accounts.models import CustomUser; CustomUser.objects.create_user(username='sassas', email='sas@example.com', password='sassas', name='SAS', role='sas') | python final_project\manage.py shell
echo from final_project.accounts.models import CustomUser; CustomUser.objects.create_user(username='dininghall', email='dininghall@example.com', password='dininghall', name='Dining Hall', role='dininghall') | python final_project\manage.py shell

python final_project\manage.py runserver

call tavenv\Scripts\deactivate.bat
pause